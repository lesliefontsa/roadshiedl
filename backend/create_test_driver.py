#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialiser Django
django.setup()

from travel.models import CustomUser

def create_test_driver():
    """Créer un chauffeur de test avec une note"""
    try:
        # Créer un nouveau chauffeur avec une note
        driver = CustomUser.objects.create_user(
            username='driver_test',
            password='driver123',
            first_name='Jean',
            last_name='Dupont',
            email='jean.dupont@roadshiel.cm',
            phone='+237 677 123 456',
            license_number='CM-2024-001234',
            rating=4.5,
            is_staff=False,
            is_active=True
        )
        
        print(f"✅ Chauffeur créé avec succès:")
        print(f"   - Username: {driver.username}")
        print(f"   - Nom complet: {driver.get_full_name()}")
        print(f"   - Email: {driver.email}")
        print(f"   - Téléphone: {driver.phone}")
        print(f"   - Permis: {driver.license_number}")
        print(f"   - Note: {driver.rating}/5")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")

if __name__ == '__main__':
    create_test_driver()