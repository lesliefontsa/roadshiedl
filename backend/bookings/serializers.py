# bookings/serializers.py
from rest_framework import serializers
from .models import Route, Trip, Booking, Payment
from vehicles.serializers import VehicleSerializer
from accounts.serializers import DriverProfileSerializer

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    driver = DriverProfileSerializer(read_only=True)
    booked_seats = serializers.ReadOnlyField()
    remaining_seats = serializers.ReadOnlyField()
    
    class Meta:
        model = Trip
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)
    trip_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_number', 'client', 'booking_date']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'