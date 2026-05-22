from django.shortcuts import render
from cars.models import Car
from django.db.models import Avg


def home(request):
    featured_cars = Car.objects.filter(is_featured=True, status='available')[:6]
    for car in featured_cars:
        avg_rating = car.reviews.aggregate(Avg('rating'))['rating__avg']
        car.avg_rating = round(avg_rating, 1) if avg_rating else None
        car.primary_image = car.images.filter(is_primary=True).first() or car.images.first()

    brands = Car.objects.values_list('brand', flat=True).distinct().order_by('brand')[:10]
    return render(request, 'home.html', {
        'featured_cars': featured_cars,
        'brands': brands,
    })
