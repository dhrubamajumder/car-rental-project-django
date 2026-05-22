from django import forms
from .models import CarReview


class CarSearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search cars...'}))
    brand = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Brand'}))
    fuel_type = forms.ChoiceField(choices=[('', 'All Fuel')] + [('petrol', 'Petrol'), ('diesel', 'Diesel'), ('ev', 'Electric'), ('hybrid', 'Hybrid')], required=False)
    transmission = forms.ChoiceField(choices=[('', 'All Transmission')] + [('manual', 'Manual'), ('auto', 'Automatic')], required=False)
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Min price'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Max price'}))
    sort_by = forms.ChoiceField(choices=[
        ('', 'Sort by'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('newest', 'Newest First'),
    ], required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }
