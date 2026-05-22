from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('ev', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('auto', 'Automatic'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    seats = models.IntegerField(default=5)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    mileage = models.CharField(max_length=50, blank=True, help_text="e.g. 18 km/l")
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    rent_per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.car}"


class CarReview(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['car', 'user']

    def __str__(self):
        return f"Review by {self.user.email} for {self.car}"
