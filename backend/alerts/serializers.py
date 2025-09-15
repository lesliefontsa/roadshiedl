# alerts/serializers.py
from rest_framework import serializers
from .models import Alert, DriverBehaviorLog
from vehicles.serializers import VehicleSerializer
from accounts.serializers import DriverProfileSerializer

class AlertSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    driver = DriverProfileSerializer(read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__'

class DriverBehaviorLogSerializer(serializers.ModelSerializer):
    driver = DriverProfileSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    
    class Meta:
        model = DriverBehaviorLog
        fields = '__all__'