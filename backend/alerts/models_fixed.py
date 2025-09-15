# alerts/models.py - Version corrigée
from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Faible'),
        ('moderate', 'Modéré'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Accusée réception'),
        ('resolved', 'Résolue'),
    ]
    
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_alerts')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_alerts')
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    timestamp = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.alert_type} - {self.driver.username} - {self.timestamp}"

class DriverBehaviorLog(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_behavior_logs')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_behavior_logs')
    fatigue_level = models.IntegerField(default=0)  # 0-10 scale
    drowsiness_events = models.IntegerField(default=0)
    speed_violations = models.IntegerField(default=0)
    harsh_braking_events = models.IntegerField(default=0)
    harsh_acceleration_events = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)  # in kilometers
    trip_duration = models.DurationField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.driver.username} - {self.timestamp}"