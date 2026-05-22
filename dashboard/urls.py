from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('cars/', views.admin_cars, name='admin_cars'),
    path('cars/add/', views.admin_add_car, name='admin_add_car'),
    path('cars/edit/<int:car_id>/', views.admin_edit_car, name='admin_edit_car'),
    path('cars/delete/<int:car_id>/', views.admin_delete_car, name='admin_delete_car'),
    path('bookings/', views.admin_bookings, name='admin_bookings'),
    path('bookings/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('bookings/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('revenue/', views.revenue_dashboard, name='revenue_dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
]
