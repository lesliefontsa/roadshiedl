# vehicles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('<int:vehicle_id>/tracking/', views.vehicle_tracking, name='vehicle_tracking'),
    path('buses/', views.list_buses, name='list_buses'),
    path('buses/create/', views.create_bus, name='create_bus'),
]