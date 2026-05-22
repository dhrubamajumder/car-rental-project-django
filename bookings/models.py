from django.db import models
from accounts.models import User
from cars.models import Car


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('online', 'Online'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    driver_service = models.BooleanField(default=False)
    insurance = models.BooleanField(default=False)
    gps = models.BooleanField(default=False)
    extra_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        from datetime import date
        delta = (self.end_date - self.start_date).days
        self.total_days = max(delta, 1)
        self.total_amount = self.total_days * self.car.rent_per_day
        self.extra_charges = 0
        if self.driver_service:
            self.extra_charges += self.total_days * 500
        if self.insurance:
            self.extra_charges += self.total_days * 300
        if self.gps:
            self.extra_charges += self.total_days * 200
        self.grand_total = self.total_amount + self.extra_charges
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.car} by {self.user.email}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('online', 'Online')], default='cash')
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for {self.booking}"
