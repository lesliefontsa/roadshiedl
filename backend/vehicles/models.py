# vehicles/models.py
from django.db import models

class Vehicle(models.Model):
    TYPE_CHOICES = [
        ('bus', 'Bus'),
        ('minibus', 'Minibus'),
        ('car', 'Voiture'),
        ('van', 'Van'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('maintenance', 'En maintenance'),
        ('out_of_service', 'Hors service'),
    ]
    
    registration_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    has_ac = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_entertainment = models.BooleanField(default=False)
    arduino_device_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.registration_number} - {self.brand} {self.model}"

class VehicleTracking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='tracking_data')
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()  # km/h
    fuel_level = models.FloatField(null=True, blank=True)  # percentage
    engine_temperature = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.timestamp}"