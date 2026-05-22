from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:car_id>/', views.create_booking, name='create_booking'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking-detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
