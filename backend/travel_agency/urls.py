# travel_agency/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib import admin as djadmin
from . import backoffice_views
from django.views.generic import TemplateView
from travel import views as travel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-backoffice/', backoffice_views.admin_backoffice, name='admin_backoffice'),
    path('admin-backoffice-fixed/', backoffice_views.admin_backoffice_fixed, name='admin_backoffice_fixed'),
    
    # Authentication URLs at root level
    path('auth/login/', travel_views.login_view, name='auth_login'),
    path('auth/logout/', travel_views.logout_view, name='auth_logout'),
    path('auth/register/', travel_views.register_view, name='auth_register'),
    
    # Dashboard URLs at root level
    path('admin-dashboard/', travel_views.admin_dashboard, name='admin_dashboard'),
    path('client-dashboard/', travel_views.client_dashboard, name='client_dashboard'),
    path('client/', travel_views.client_dashboard_view, name='client_dashboard_view'),
    
    # API endpoints at root level  
    path('api/auth/login/', travel_views.api_login_view, name='api_auth_login'),
    path('api/auth/register/', travel_views.register_view, name='api_auth_register'),
    path('api/trips/', travel_views.api_trips, name='api_trips'),
    path('api/bookings/create/', travel_views.api_create_booking, name='api_create_booking'),
    path('api/arduino/alerts/', travel_views.api_arduino_alert, name='api_arduino_alert'),
    path('api/drivers/create/', travel_views.create_driver_view, name='api_create_driver'),
    path('api/buses/create/', travel_views.create_bus_view, name='api_create_bus'),
    path('api/trips/create/', travel_views.create_trip_view, name='api_create_trip'),
    path('api/trips/list/', travel_views.list_trips_view, name='api_list_trips'),
    path('api/trips/test/', travel_views.test_trips_view, name='api_test_trips'),
    path('api/payment/process/', travel_views.process_payment_view, name='api_process_payment'),
    path('api/payment/create-intent/', travel_views.create_payment_intent_view, name='api_create_payment_intent'),
    path('api/booking/confirm/', travel_views.confirm_booking_view, name='api_confirm_booking'),
    path('api/bookings/list/', travel_views.list_user_bookings_view, name='api_list_bookings'),
    path('api/invoice/download/<str:invoice_number>/', travel_views.download_invoice_view, name='api_download_invoice'),
    
    # Servir l'interface web depuis Django
    path('', TemplateView.as_view(template_name='login-dual.html'), name='login_page'),
    path('test-debug/', TemplateView.as_view(template_name='test-debug.html'), name='test_debug'),
    path('test-api/', TemplateView.as_view(template_name='test-api.html'), name='test_api'),
    path('login-fixed/', TemplateView.as_view(template_name='login-fixed.html'), name='login_fixed'),
    path('test-logout/', TemplateView.as_view(template_name='test-logout.html'), name='test_logout'),
    path('test-redirection/', TemplateView.as_view(template_name='test-redirection.html'), name='test_redirection'),
    
    # Include travel app URLs under /travel/ for backoffice
    path('travel/', include('travel.urls')),
]

# Include accounts urls only if the app is enabled in INSTALLED_APPS
if 'accounts' in getattr(settings, 'INSTALLED_APPS', []):
    urlpatterns += [
        path('accounts/', include('accounts.urls')),
    ]

# Servir les fichiers média en mode développement
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)