from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile, User
from cars.models import Car
from django.db.models import Avg


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# def user_login(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=email, password=password)
#             if user and not user.is_blocked:
#                 login(request, user)
#                 messages.success(request, f'Welcome back, {user.email}!')
#                 next_url = request.GET.get('next', 'home')
#                 return redirect(next_url)
#             elif user and user.is_blocked:
#                 messages.error(request, 'Your account has been blocked.')
#             else:
#                 messages.error(request, 'Invalid credentials.')
#     else:
#         form = UserLoginForm()
#     return render(request, 'accounts/login.html', {'form': form})


# ================= USER LOGIN =================
def user_login(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard_home')
        return redirect('home')

    form = UserLoginForm(request, data=request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user:

                # ❌ ADMIN trying user login
                if user.is_superuser:
                    messages.error(
                        request,
                        "⛔ Admin accounts cannot login from User Login page. Please use Admin Login."
                    )

                # ❌ BLOCKED USER
                elif user.is_blocked:
                    messages.error(
                        request,
                        "🚫 Your account is blocked. Contact support."
                    )

                # ✅ SUCCESS USER LOGIN
                else:
                    login(request, user)
                    messages.success(
                        request,
                        f"Welcome back, {user.email}!"
                    )
                    return redirect('home')

            else:
                messages.error(
                    request,
                    "❌ Invalid email or password."
                )

    return render(request, 'accounts/login.html', {
        'form': form,
        'is_admin': False
    })


# ================= ADMIN LOGIN =================
def admin_login(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard_home')
        return redirect('home')

    form = UserLoginForm(request, data=request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user:

                # ❌ USER trying admin login
                if not user.is_superuser:
                    messages.error(
                        request,
                        "⛔ Access denied! Only administrators can login here."
                    )

                # ❌ BLOCKED ADMIN
                elif user.is_blocked:
                    messages.error(
                        request,
                        "🚫 Your admin account is blocked."
                    )

                # ✅ SUCCESS ADMIN LOGIN
                else:
                    login(request, user)
                    messages.success(
                        request,
                        f"Welcome Admin, {user.email}!"
                    )
                    return redirect('dashboard_home')

            else:
                messages.error(
                    request,
                    "❌ Invalid admin credentials."
                )

    return render(request, 'accounts/admin_login.html', {
        'form': form,
        'is_admin': True
    })
    
    

def user_logout(request):
    user = request.user
    logout(request)
    # ================= ROLE CHECK =================
    if user.is_superuser:
        messages.info(request, 'Admin logged out successfully.')
        return redirect('admin_login')
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        # ✅ template decide
    if request.user.is_staff or request.user.is_superuser:
        template = 'admin.html'
    else:
        template = 'base.html'
    return render(request, 'accounts/profile.html', {'u_form': u_form, 'p_form': p_form, 'template': template})


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
