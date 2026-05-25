from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cars.models import Car
from .models import Booking, Payment
from .forms import BookingForm
from notifications.models import Notification


@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id, status='available')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save()
            Notification.objects.create(
                user=request.user,
                title='Booking Submitted',
                message=f'Your booking for {car.brand} {car.model} has been submitted and is pending approval.',
                notification_type='booking'
            )
            messages.success(request, 'Booking created successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'car': car, 'form': form})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    active = bookings.exclude(status__in=['cancelled', 'completed'])
    past = bookings.filter(status__in=['cancelled', 'completed'])
    return render(request, 'bookings/my_bookings.html', {
        'active': active,
        'past': past,
    })


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status in ['pending', 'approved']:
        booking.status = 'cancelled'
        booking.save()

        Notification.objects.create(
            user=request.user,
            title='Booking Cancelled',
            message=f'Your booking #{booking.id} for {booking.car} has been cancelled.',
            notification_type='booking'
        )

        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    return redirect('my_bookings')
