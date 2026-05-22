from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    path('<int:car_id>/add-review/', views.add_review, name='add_review'),
]
