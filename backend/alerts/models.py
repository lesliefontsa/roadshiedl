# alerts/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('drowsiness', 'Somnolence'),
        ('fatigue', 'Fatigue'),
        ('speeding', 'Excès de vitesse'),
        ('harsh_braking', 'Freinage brusque'),
        ('harsh_acceleration', 'Accélération brusque'),
        ('route_deviation', 'Déviation de route'),
        ('vehicle_breakdown', 'Panne véhicule'),
        ('emergency', 'Urgence'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Modéré'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('acknowledged', 'Accusé réception'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
        ('dismissed', 'Rejeté'),
    ]
    
    # Utilisation de string référence pour éviter les dépendances circulaires
    vehicle_name = models.CharField(max_length=100, default="Véhicule")
    driver_name = models.CharField(max_length=100, default="Conducteur")
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    message = models.TextField()
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    speed_at_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acknowledged_alerts')
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    arduino_data = models.JSONField(null=True, blank=True)  # Raw data from Arduino
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.vehicle_name} - {self.created_at}"