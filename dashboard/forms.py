from django import forms
from cars.models import Car, CarImage


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'seats', 'fuel_type', 'transmission', 'mileage', 'rent_per_day', 'rent_per_hour', 'description', 'location', 'status', 'is_featured']


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image', 'is_primary']


class BookingFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[
        ('', 'All Status'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], required=False)
