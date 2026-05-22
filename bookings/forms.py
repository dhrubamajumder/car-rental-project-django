from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'driver_service', 'insurance', 'gps']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and start >= end:
            raise forms.ValidationError("End date must be after start date.")
        from datetime import date
        if start and start < date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        return cleaned_data
