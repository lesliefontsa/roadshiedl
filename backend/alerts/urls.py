# alerts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlertListView.as_view(), name='alert_list'),
    path('<int:alert_id>/acknowledge/', views.acknowledge_alert, name='acknowledge_alert'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
]