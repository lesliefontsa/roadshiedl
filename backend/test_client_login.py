#!/usr/bin/env python3
import os
import django
import sys

# Ajouter le répertoire du projet au Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from travel.models import CustomUser

print("=== Vérification des utilisateurs ===")

# Lister tous les utilisateurs
users = CustomUser.objects.all()
print(f"Nombre total d'utilisateurs: {users.count()}")

for user in users:
    print(f"- {user.username} (email: {user.email}, role: {user.role}, staff: {user.is_staff})")

# Vérifier spécifiquement client1
try:
    client = CustomUser.objects.get(username='client1')
    print(f"\n✅ client1 trouvé:")
    print(f"   - Email: {client.email}")
    print(f"   - Nom: {client.first_name} {client.last_name}")
    print(f"   - Role: {client.role}")
    print(f"   - Staff: {client.is_staff}")
    print(f"   - Mot de passe configuré: {bool(client.password)}")
    
    # Tester la vérification du mot de passe
    if client.check_password('client123'):
        print("   - ✅ Mot de passe 'client123' correct")
    else:
        print("   - ❌ Mot de passe 'client123' incorrect")
        
except CustomUser.DoesNotExist:
    print("\n❌ client1 n'existe pas. Création en cours...")
    client = CustomUser.objects.create_user(
        username='client1',
        email='client1@test.com',
        password='client123',
        first_name='Client',
        last_name='Test',
        role='client'
    )
    print("✅ client1 créé avec succès!")

print("\n=== Test de connexion terminé ===")