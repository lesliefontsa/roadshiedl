# setup_database.py
"""
Script de configuration de la base de données PostgreSQL
pour RoadShield Travel Agency
"""

import os
import django
import sys

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from travel.models import Bus, Trip, CustomUser
from datetime import datetime, date, time
from decimal import Decimal

def create_superuser():
    """Créer un superutilisateur admin"""
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@roadshield.cm',
            password='admin123',
            first_name='Administrateur',
            last_name='Principal',
            role='admin'
        )
        print("✅ Superutilisateur 'admin' créé avec succès")
    else:
        print("ℹ️  Superutilisateur 'admin' existe déjà")

def create_test_users():
    """Créer des utilisateurs de test"""
    User = get_user_model()
    
    test_users = [
        {
            'username': 'manager',
            'email': 'manager@roadshield.cm',
            'password': 'manager123',
            'first_name': 'Manager',
            'last_name': 'Transport',
            'role': 'admin'
        },
        {
            'username': 'client1',
            'email': 'client1@example.com',
            'password': 'client123',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'role': 'client'
        },
        {
            'username': 'marie',
            'email': 'marie@example.com',
            'password': 'marie123',
            'first_name': 'Marie',
            'last_name': 'Ngono',
            'role': 'client'
        },
        {
            'username': 'paul',
            'email': 'paul@example.com',
            'password': 'paul123',
            'first_name': 'Paul',
            'last_name': 'Mbassa',
            'role': 'client'
        }
    ]
    
    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            User.objects.create_user(**user_data)
            print(f"✅ Utilisateur '{user_data['username']}' créé")
        else:
            print(f"ℹ️  Utilisateur '{user_data['username']}' existe déjà")

def create_test_buses():
    """Créer des bus de test"""
    buses_data = [
        {
            'bus_number': 'RD-001',
            'bus_model': 'Mercedes Sprinter',
            'total_seats': 50,
            'year': 2023,
            'status': 'disponible',
            'mileage': 25000,
            'notes': 'Bus principal pour les longs trajets'
        },
        {
            'bus_number': 'RD-002',
            'bus_model': 'Iveco Daily',
            'total_seats': 45,
            'year': 2022,
            'status': 'disponible',
            'mileage': 18000,
            'notes': 'Bus de luxe avec climatisation'
        },
        {
            'bus_number': 'RD-003',
            'bus_model': 'Toyota Hiace',
            'total_seats': 25,
            'year': 2021,
            'status': 'maintenance',
            'mileage': 45000,
            'notes': 'Entretien programmé'
        }
    ]
    
    for bus_data in buses_data:
        if not Bus.objects.filter(bus_number=bus_data['bus_number']).exists():
            Bus.objects.create(**bus_data)
            print(f"✅ Bus '{bus_data['bus_number']}' créé")
        else:
            print(f"ℹ️  Bus '{bus_data['bus_number']}' existe déjà")

def create_test_trips():
    """Créer des voyages de test"""
    admin_user = CustomUser.objects.get(username='admin')
    bus1 = Bus.objects.get(bus_number='RD-001')
    bus2 = Bus.objects.get(bus_number='RD-002')
    
    from datetime import timedelta
    tomorrow = date.today() + timedelta(days=1)
    day_after = date.today() + timedelta(days=2)
    
    trips_data = [
        {
            'departure_city': 'Yaoundé',
            'arrival_city': 'Douala',
            'date': tomorrow,
            'departure_time': time(8, 0),
            'duration': '4h30',
            'bus': bus1,
            'price_simple': Decimal('5000'),
            'price_return': Decimal('9000'),
            'notes': 'Voyage direct avec arrêt Édéa',
            'created_by': admin_user
        },
        {
            'departure_city': 'Douala',
            'arrival_city': 'Bamenda',
            'date': day_after,
            'departure_time': time(10, 0),
            'duration': '5h00',
            'bus': bus2,
            'price_simple': Decimal('7500'),
            'price_return': Decimal('13500'),
            'notes': 'Route panoramique',
            'created_by': admin_user
        }
    ]
    
    for trip_data in trips_data:
        if not Trip.objects.filter(
            departure_city=trip_data['departure_city'],
            arrival_city=trip_data['arrival_city'],
            date=trip_data['date']
        ).exists():
            Trip.objects.create(**trip_data)
            print(f"✅ Voyage '{trip_data['departure_city']} → {trip_data['arrival_city']}' créé")
        else:
            print(f"ℹ️  Voyage '{trip_data['departure_city']} → {trip_data['arrival_city']}' existe déjà")

def main():
    """Fonction principale de configuration"""
    print("🚀 Configuration de la base de données RoadShield Travel")
    print("=" * 60)
    
    try:
        # Migrations
        print("\n📦 Application des migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Création des données de test
        print("\n👤 Création des utilisateurs...")
        create_superuser()
        create_test_users()
        
        print("\n🚌 Création des bus...")
        create_test_buses()
        
        print("\n🛣️  Création des voyages...")
        create_test_trips()
        
        print("\n" + "=" * 60)
        print("✅ Configuration terminée avec succès !")
        print("\n🌐 Comptes disponibles :")
        print("   👨‍💼 Admin: admin / admin123")
        print("   👨‍💼 Manager: manager / manager123")
        print("   👤 Client: client1 / client123")
        print("   👤 Client: marie / marie123")
        print("   👤 Client: paul / paul123")
        print("\n🔗 URL de connexion: http://localhost:8002/auth/login/")
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()