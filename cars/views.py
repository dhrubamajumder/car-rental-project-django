from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Car, CarImage, CarReview
from .forms import CarSearchForm, ReviewForm


def car_list(request):
    cars = Car.objects.filter(status='available')
    form = CarSearchForm(request.GET)

    if form.is_valid():
        search = form.cleaned_data.get('search')
        brand = form.cleaned_data.get('brand')
        fuel_type = form.cleaned_data.get('fuel_type')
        transmission = form.cleaned_data.get('transmission')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        sort_by = form.cleaned_data.get('sort_by')

        if search:
            cars = cars.filter(
                Q(brand__icontains=search) |
                Q(model__icontains=search) |
                Q(location__icontains=search)
            )
        if brand:
            cars = cars.filter(brand__icontains=brand)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)
        if transmission:
            cars = cars.filter(transmission=transmission)
        if min_price:
            cars = cars.filter(rent_per_day__gte=min_price)
        if max_price:
            cars = cars.filter(rent_per_day__lte=max_price)

        if sort_by == 'price_asc':
            cars = cars.order_by('rent_per_day')
        elif sort_by == 'price_desc':
            cars = cars.order_by('-rent_per_day')
        elif sort_by == 'newest':
            cars = cars.order_by('-created_at')

    brands = Car.objects.values_list('brand', flat=True).distinct().order_by('brand')

    for car in cars:
        avg_rating = car.reviews.aggregate(Avg('rating'))['rating__avg']
        car.avg_rating = round(avg_rating, 1) if avg_rating else None
        car.primary_image = car.images.filter(is_primary=True).first() or car.images.first()

    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'form': form,
        'brands': brands,
    })


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    images = car.images.all()
    reviews = car.reviews.select_related('user').all()
    avg_rating = car.reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'images': images,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'review_form': ReviewForm(),
    })


@login_required
def add_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            messages.success(request, 'Review added!')
    return redirect('car_detail', car_id=car.id)
