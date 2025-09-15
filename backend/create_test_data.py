#!/usr/bin/env python
"""
Script pour créer des données de test
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from travel.models import CustomUser, Bus, Trip

def create_test_data():
    print("🚀 Création des données de test...")
    
    # Créer des bus de test
    buses = [
        {
            'bus_number': 'CM-1234-AB',
            'bus_model': 'Mercedes Sprinter',
            'total_seats': 50,
            'year': 2020,
            'status': 'disponible'
        },
        {
            'bus_number': 'CM-5678-CD',
            'bus_model': 'Volvo 9700',
            'total_seats': 55,
            'year': 2019,
            'status': 'disponible'
        },
        {
            'bus_number': 'CM-9012-EF',
            'bus_model': 'Scania Touring',
            'total_seats': 60,
            'year': 2021,
            'status': 'disponible'
        }
    ]
    
    for bus_data in buses:
        bus, created = Bus.objects.get_or_create(
            bus_number=bus_data['bus_number'],
            defaults=bus_data
        )
        if created:
            print(f"✅ Bus créé: {bus.bus_number} - {bus.bus_model}")
    
    # Créer des chauffeurs de test
    drivers = [
        {
            'username': 'jean_dupont',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.dupont@roadshield.com',
            'role': 'driver',
            'license_number': 'LIC123456',
            'experience_years': 8,
            'rating': 4.5
        },
        {
            'username': 'marie_martin',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'email': 'marie.martin@roadshield.com',
            'role': 'driver',
            'license_number': 'LIC789012',
            'experience_years': 5,
            'rating': 4.2
        }
    ]
    
    for driver_data in drivers:
        driver, created = CustomUser.objects.get_or_create(
            username=driver_data['username'],
            defaults=driver_data
        )
        if created:
            driver.set_password('roadshield123')
            driver.save()
            print(f"✅ Chauffeur créé: {driver.first_name} {driver.last_name}")
    
    # Créer des voyages de test
    tomorrow = datetime.now().date() + timedelta(days=1)
    next_week = datetime.now().date() + timedelta(days=7)
    
    trips = [
        {
            'trip_number': 'TRP1001',
            'departure_city': 'Douala',
            'arrival_city': 'Yaoundé',
            'date': tomorrow,
            'departure_time': '08:00',
            'price_simple': 5000,
            'price_return': 9000,
            'max_seats': 50,
            'bus': Bus.objects.get(bus_number='CM-1234-AB'),
            'driver': CustomUser.objects.get(username='jean_dupont'),
            'created_by': CustomUser.objects.get(username='jean_dupont')
        },
        {
            'trip_number': 'TRP1002',
            'departure_city': 'Yaoundé',
            'arrival_city': 'Bafoussam',
            'date': tomorrow,
            'departure_time': '14:00',
            'price_simple': 3500,
            'price_return': 6500,
            'max_seats': 55,
            'bus': Bus.objects.get(bus_number='CM-5678-CD'),
            'driver': CustomUser.objects.get(username='marie_martin'),
            'created_by': CustomUser.objects.get(username='marie_martin')
        },
        {
            'trip_number': 'TRP1003',
            'departure_city': 'Douala',
            'arrival_city': 'Bamenda',
            'date': next_week,
            'departure_time': '06:30',
            'price_simple': 4500,
            'price_return': 8000,
            'max_seats': 60,
            'bus': Bus.objects.get(bus_number='CM-9012-EF'),
            'driver': CustomUser.objects.get(username='jean_dupont'),
            'created_by': CustomUser.objects.get(username='jean_dupont')
        },
        {
            'trip_number': 'TRP1004',
            'departure_city': 'Yaoundé',
            'arrival_city': 'Garoua',
            'date': next_week,
            'departure_time': '20:00',
            'price_simple': 8000,
            'price_return': 15000,
            'max_seats': 50,
            'bus': Bus.objects.get(bus_number='CM-1234-AB'),
            'driver': CustomUser.objects.get(username='marie_martin'),
            'created_by': CustomUser.objects.get(username='marie_martin')
        }
    ]
    
    for trip_data in trips:
        trip, created = Trip.objects.get_or_create(
            trip_number=trip_data['trip_number'],
            defaults=trip_data
        )
        if created:
            print(f"✅ Voyage créé: {trip.trip_number} - {trip.departure_city} → {trip.arrival_city}")
    
    # Créer un utilisateur client de test
    client, created = CustomUser.objects.get_or_create(
        username='client_test',
        defaults={
            'first_name': 'Client',
            'last_name': 'Test',
            'email': 'client@test.com',
            'role': 'client',
            'phone': '+237 690 123 456'
        }
    )
    if created:
        client.set_password('test123')
        client.save()
        print(f"✅ Client de test créé: {client.username}")
    
    print("\n🎉 Données de test créées avec succès !")
    print("\nComptes créés :")
    print("- Admin : utilisez votre compte existant")
    print("- Client de test : client_test / test123")
    print("- Chauffeurs : jean_dupont / roadshield123, marie_martin / roadshield123")

if __name__ == '__main__':
    create_test_data()