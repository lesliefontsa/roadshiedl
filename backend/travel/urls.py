# travel/urls.py
from django.urls import path
from . import views
from . import backoffice_views

app_name = 'travel'

urlpatterns = [
    # Authentification
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),
    
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-backoffice/', views.admin_backoffice, name='admin_backoffice'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    
    # API endpoints (pour le frontend JavaScript)
    path('api/auth/login/', views.login_view, name='api_login'),  # Same view, different URL
    path('api/auth/register/', views.register_view, name='api_register'),  # Same view, different URL
    path('api/trips/', views.api_trips, name='api_trips'),
    path('api/bookings/create/', views.api_create_booking, name='api_create_booking'),
    path('api/arduino/alerts/', views.api_arduino_alert, name='api_arduino_alert'),
    path('api/drivers/create/', views.create_driver_view, name='api_create_driver'),
    path('api/buses/create/', views.create_bus_view, name='api_create_bus'),
    path('api/trips/create/', views.create_trip_view, name='api_create_trip'),
    path('api/trips/list/', views.list_trips_view, name='api_list_trips'),
    path('api/payment/process/', views.process_payment_view, name='api_process_payment'),
    path('api/bookings/list/', views.list_user_bookings_view, name='api_list_bookings'),
    
    # Backoffice visual pages
    path('admin-backoffice/buses/', backoffice_views.backoffice_buses, name='backoffice_buses'),
    path('admin-backoffice/buses/delete/<int:bus_id>/', backoffice_views.backoffice_bus_delete, name='backoffice_bus_delete'),
    path('admin-backoffice/drivers/', backoffice_views.backoffice_drivers, name='backoffice_drivers'),
    path('admin-backoffice/trips/', backoffice_views.backoffice_trips, name='backoffice_trips'),
    path('admin-backoffice/trips/delete/<int:trip_id>/', backoffice_views.backoffice_trip_delete, name='backoffice_trip_delete'),
    path('admin-backoffice/alerts/', backoffice_views.backoffice_alerts, name='backoffice_alerts'),
]