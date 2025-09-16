#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from travel.models import CustomUser

try:
    # Créer un utilisateur admin de test
    admin_user = CustomUser.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='admin123',
        role='admin'
    )
    print("✅ Utilisateur admin créé: admin/admin123")
    
    # Créer un utilisateur client de test
    client_user = CustomUser.objects.create_user(
        username='client',
        email='client@test.com', 
        password='client123',
        role='client'
    )
    print("✅ Utilisateur client créé: client/client123")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    
print("\n🎯 Comptes utilisateur créés pour la présentation !")
print("Admin: admin/admin123")
print("Client: client/client123")