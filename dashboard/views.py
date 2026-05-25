from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from cars.models import Car, CarImage
from bookings.models import Booking
from accounts.models import User
from notifications.models import Notification
from .forms import CarForm, CarImageForm


@staff_member_required
def dashboard_home(request):
    total_cars = Car.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    active_rentals = Booking.objects.filter(status='approved').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    recent_bookings = Booking.objects.select_related('user', 'car').order_by('-created_at')[:5]

    total_car_views = 0
    conversion_rate = 0

    if total_car_views > 0:
        conversion_rate = round((total_bookings / total_car_views) * 100, 2)

    booking_status_counts = Booking.objects.values('status').annotate(count=Count('id'))

    monthly_bookings = Booking.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

    return render(request, 'dashboard/home.html', {
        'total_cars': total_cars,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'active_rentals': active_rentals,
        'pending_bookings': pending_bookings,
        'recent_bookings': recent_bookings,
        'conversion_rate': conversion_rate,
        'booking_status_counts': booking_status_counts,
        'monthly_bookings': monthly_bookings,
    })


@staff_member_required
def admin_cars(request):
    cars = Car.objects.prefetch_related('images').order_by('-created_at')
    return render(request, 'dashboard/car_list.html', {'cars': cars})



@staff_member_required
def admin_add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                CarImage.objects.create(car=car, image=img, is_primary=(i == 0))
            messages.success(request, 'Car added successfully!')
            return redirect('admin_cars')
    else:
        form = CarForm()
    return render(request, 'dashboard/car_form.html', {'form': form, 'title': 'Add Car'})


@staff_member_required
def admin_edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            car = form.save()
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                CarImage.objects.create(car=car, image=img, is_primary=(i == 0 and not car.images.filter(is_primary=True).exists()))
            messages.success(request, 'Car updated!')
            return redirect('admin_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'dashboard/car_form.html', {'form': form, 'title': 'Edit Car', 'car': car})


@staff_member_required
def admin_delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, 'Car deleted.')
    return redirect('admin_cars')


@staff_member_required
def admin_bookings(request):
    bookings = Booking.objects.select_related('user', 'car').all().order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'dashboard/booking_list.html', {'bookings': bookings})


@staff_member_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'approved'
    booking.save()
    booking.car.status = 'booked'
    booking.car.save()

    Notification.objects.create(
        user=booking.user,
        title='Booking Approved',
        message=f'Your booking #{booking.id} for {booking.car} has been approved!',
        notification_type='booking'
    )
    messages.success(request, f'Booking #{booking.id} approved.')
    return redirect('admin_bookings')


@staff_member_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'rejected'
    booking.save()

    Notification.objects.create(
        user=booking.user,
        title='Booking Rejected',
        message=f'Your booking #{booking.id} for {booking.car} has been rejected.',
        notification_type='booking'
    )
    messages.success(request, f'Booking #{booking.id} rejected.')
    return redirect('admin_bookings')


@staff_member_required
def admin_users(request):
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})


@staff_member_required
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = True
    user.save()
    messages.success(request, f'{user.email} blocked.')
    return redirect('admin_users')


@staff_member_required
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = False
    user.save()
    messages.success(request, f'{user.email} unblocked.')
    return redirect('admin_users')


@staff_member_required
def revenue_dashboard(request):
    total_revenue = Booking.objects.filter(status__in=['approved', 'completed']).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    monthly_revenue = (
        Booking.objects.filter(status__in=['approved', 'completed'])
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('grand_total'))
        .order_by('month')
    )
    daily_earnings = (
        Booking.objects.filter(status__in=['approved', 'completed'], created_at__gte=timezone.now() - timedelta(days=30))
        .extra(select={'day': "date(created_at)"})
        .values('day')
        .annotate(total=Sum('grand_total'))
        .order_by('day')
    )
    top_cars = (
        Car.objects.annotate(total_revenue=Sum('bookings__grand_total', filter=Q(bookings__status__in=['approved', 'completed'])))
        .order_by('-total_revenue')[:10]
    )
    pending_payments = Booking.objects.filter(payment_status='pending').count()

    return render(request, 'dashboard/revenue.html', {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'daily_earnings': daily_earnings,
        'top_cars': top_cars,
        'pending_payments': pending_payments,
    })


@staff_member_required
def analytics_dashboard(request):
    total_cars = Car.objects.count()
    total_bookings = Booking.objects.count()
    active_rentals = Booking.objects.filter(status='approved').count()
    total_car_views = 0
    conversion_rate = 0
    if total_car_views > 0:
        conversion_rate = round((total_bookings / total_car_views) * 100, 2)

    booking_status_counts = Booking.objects.values('status').annotate(count=Count('id'))
    monthly_bookings = (
        Booking.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    return render(request, 'dashboard/analytics.html', {
        'total_cars': total_cars,
        'total_bookings': total_bookings,
        'active_rentals': active_rentals,
        'conversion_rate': conversion_rate,
        'booking_status_counts': booking_status_counts,
        'monthly_bookings': monthly_bookings,
    })
