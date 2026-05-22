from django.contrib import admin
from .models import Car, CarImage, CarReview


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


class CarReviewInline(admin.TabularInline):
    model = CarReview
    extra = 0


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'fuel_type', 'transmission', 'rent_per_day', 'status')
    list_filter = ('status', 'fuel_type', 'transmission', 'brand')
    search_fields = ('brand', 'model', 'location')
    inlines = [CarImageInline, CarReviewInline]


admin.site.register(CarImage)
admin.site.register(CarReview)
