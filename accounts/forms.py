from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'profile_picture', 'driving_license', 'address', 'city', 'state', 'zip_code', 'saved_addresses']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'saved_addresses': forms.Textarea(attrs={'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']
