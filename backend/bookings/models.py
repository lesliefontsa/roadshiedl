# bookings/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Route(models.Model):
    name = models.CharField(max_length=200)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    distance_km = models.FloatField()
    estimated_duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.departure_city} → {self.arrival_city}"

class Trip(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Programmé'),
        ('boarding', 'Embarquement'),
        ('in_transit', 'En route'),
        ('arrived', 'Arrivé'),
        ('cancelled', 'Annulé'),
        ('delayed', 'Retardé'),
    ]
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE)
    driver = models.ForeignKey('accounts.DriverProfile', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.route} - {self.departure_time.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def booked_seats(self):
        return self.bookings.filter(status__in=['confirmed', 'checked_in']).count()
    
    @property
    def remaining_seats(self):
        return self.available_seats - self.booked_seats

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('checked_in', 'Enregistré'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
        ('no_show', 'Absent'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('failed', 'Échec'),
        ('refunded', 'Remboursé'),
    ]
    
    booking_number = models.CharField(max_length=20, unique=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=200)
    passenger_phone = models.CharField(max_length=20)
    passenger_email = models.EmailField()
    seat_number = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    special_requests = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['trip', 'seat_number']
    
    def __str__(self):
        return f"{self.booking_number} - {self.passenger_name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_number:
            import random
            import string
            self.booking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('card', 'Carte bancaire'),
        ('mobile', 'Mobile Money'),
        ('bank_transfer', 'Virement bancaire'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount}€"