# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('routes/', views.RouteListView.as_view(), name='route_list'),
    path('trips/search/', views.TripSearchView.as_view(), name='trip_search'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
]