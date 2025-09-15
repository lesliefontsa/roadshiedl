# vehicles/serializers.py
from rest_framework import serializers
from .models import Vehicle, VehicleTracking

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleTrackingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    
    class Meta:
        model = VehicleTracking
        fields = '__all__'