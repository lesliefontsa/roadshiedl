#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append('c:/Users/user/RoadShiel Sentinelle/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from travel.models import CustomUser

# Créer un utilisateur client
try:
    # Supprimer l'utilisateur s'il existe déjà
    try:
        user = CustomUser.objects.get(username='client')
        user.delete()
        print("Utilisateur 'client' existant supprimé")
    except CustomUser.DoesNotExist:
        pass
    
    # Créer le nouvel utilisateur client
    client_user = CustomUser.objects.create_user(
        username='client',
        email='client@test.com',
        password='client123',
        first_name='Test',
        last_name='Client',
        is_staff=False,  # Important: pas un admin
        is_active=True
    )
    
    print(f"Utilisateur client créé avec succès: {client_user.username}")
    print(f"is_staff: {client_user.is_staff}")
    print(f"is_active: {client_user.is_active}")
    
except Exception as e:
    print(f"Erreur lors de la création: {e}")