#!/bin/bash

# Script de démarrage pour l'application Travel Agency

echo "=== Démarrage de RoadShield Travel Agency ==="

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python -m venv venv
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate  # Pour Linux/Mac
# Pour Windows, utilisez: venv\Scripts\activate.bat

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Changer vers le répertoire backend
cd backend

# Effectuer les migrations
echo "Application des migrations..."
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur si nécessaire
echo "Création du superutilisateur (si nécessaire)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur existe déjà')
"

# Charger des données de test
echo "Chargement des données de test..."
python manage.py shell -c "
import os
import django
from vehicles.models import Vehicle
from accounts.models import User, DriverProfile
from bookings.models import Route

# Créer des véhicules de test
if not Vehicle.objects.exists():
    vehicles = [
        Vehicle.objects.create(
            registration_number='TRK-001',
            brand='Renault',
            model='Master',
            year=2022,
            vehicle_type='bus',
            capacity=50,
            has_ac=True,
            has_wifi=True,
            arduino_device_id='ARDUINO_001'
        ),
        Vehicle.objects.create(
            registration_number='TRK-002',
            brand='Mercedes',
            model='Sprinter',
            year=2023,
            vehicle_type='minibus',
            capacity=25,
            has_ac=True,
            has_wifi=False,
            arduino_device_id='ARDUINO_002'
        ),
        Vehicle.objects.create(
            registration_number='TRK-003',
            brand='Ford',
            model='Transit',
            year=2021,
            vehicle_type='van',
            capacity=15,
            has_ac=False,
            has_wifi=False,
            arduino_device_id='ARDUINO_003'
        ),
    ]
    print('Véhicules de test créés')

# Créer des chauffeurs de test
if not User.objects.filter(role='driver').exists():
    drivers_data = [
        {'username': 'emmanuel', 'first_name': 'Emmanuel', 'last_name': 'Arthur', 'license': 'LIC001'},
        {'username': 'ayina', 'first_name': 'Ayina', 'last_name': 'Kone', 'license': 'LIC002'},
        {'username': 'syntyche', 'first_name': 'Syntyche', 'last_name': 'Mballa', 'license': 'LIC003'},
    ]
    
    vehicles = Vehicle.objects.all()
    for i, driver_data in enumerate(drivers_data):
        user = User.objects.create_user(
            username=driver_data['username'],
            first_name=driver_data['first_name'],
            last_name=driver_data['last_name'],
            email=f\"{driver_data['username']}@roadshield.com\",
            password='driver123',
            role='driver'
        )
        DriverProfile.objects.create(
            user=user,
            license_number=driver_data['license'],
            license_expiry='2025-12-31',
            experience_years=5 + i,
            current_vehicle=vehicles[i] if i < len(vehicles) else None
        )
    print('Chauffeurs de test créés')

# Créer des routes de test
if not Route.objects.exists():
    routes = [
        Route.objects.create(
            name='Paris - Lyon',
            departure_city='Paris',
            arrival_city='Lyon',
            distance_km=462,
            estimated_duration='04:30:00'
        ),
        Route.objects.create(
            name='Lyon - Marseille',
            departure_city='Lyon',
            arrival_city='Marseille',
            distance_km=314,
            estimated_duration='03:15:00'
        ),
        Route.objects.create(
            name='Paris - Nice',
            departure_city='Paris',
            arrival_city='Nice',
            distance_km=933,
            estimated_duration='09:30:00'
        ),
    ]
    print('Routes de test créées')

print('Données de test chargées avec succès')
"

echo "=== Application prête à démarrer ==="
echo ""
echo "Pour démarrer les serveurs:"
echo "1. Serveur Django (dans un terminal):"
echo "   cd backend && python manage.py runserver 8002"
echo ""
echo "2. Serveur FastAPI (dans un autre terminal):"
echo "   cd backend && python api/fastapi_app.py"
echo ""
echo "3. Ouvrir dans le navigateur:"
echo "   - Client: http://localhost:8002/client.html"
echo "   - Admin: http://localhost:8002/index.html"
echo "   - API Docs: http://localhost:8003/docs"
echo ""
echo "Comptes de test:"
echo "- Admin: admin/admin123"
echo "- Chauffeurs: emmanuel/driver123, ayina/driver123, syntyche/driver123"