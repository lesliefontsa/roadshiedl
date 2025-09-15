#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from alerts.models import Alert

# Create test alerts
alerts_data = [
    {
        'vehicle_name': 'Bus A123',
        'driver_name': 'Jean Dupont',
        'alert_type': 'drowsiness',
        'severity': 'high',
        'message': 'Détection de somnolence du conducteur',
        'speed_at_time': 85.5
    },
    {
        'vehicle_name': 'Bus B456',
        'driver_name': 'Marie Martin',
        'alert_type': 'speeding',
        'severity': 'medium',
        'message': 'Dépassement de la vitesse autorisée',
        'speed_at_time': 95.0
    },
    {
        'vehicle_name': 'Bus C789',
        'driver_name': 'Pierre Leroy',
        'alert_type': 'harsh_braking',
        'severity': 'low',
        'message': 'Freinage brusque détecté',
        'speed_at_time': 45.2
    },
    {
        'vehicle_name': 'Bus D321',
        'driver_name': 'Sophie Blanc',
        'alert_type': 'emergency',
        'severity': 'critical',
        'message': 'Situation d\'urgence - intervention requise',
        'speed_at_time': 0.0
    }
]

# Delete existing alerts
Alert.objects.all().delete()

# Create new alerts
for alert_data in alerts_data:
    Alert.objects.create(**alert_data)

print(f"Créé {len(alerts_data)} alertes de test")