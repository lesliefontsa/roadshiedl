#!/usr/bin/env python
"""
Test direct de l'API list_trips_view
"""

import os
import sys
import django
import requests

# Ajouter le répertoire du projet au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

def test_api_direct():
    """Test direct de l'API"""
    print("🧪 Test de l'API /api/trips/list/")
    
    try:
        # Test avec requests
        response = requests.get('http://127.0.0.1:8009/api/trips/list/', timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            json_data = response.json()
            print(f"Response JSON: {json_data}")
            
            if json_data.get('status') == 'success':
                trips = json_data.get('trips', [])
                print(f"✅ API fonctionne! {len(trips)} voyages trouvés")
                
                for trip in trips[:2]:  # Afficher les 2 premiers
                    print(f"  - {trip.get('trip_number')}: {trip.get('route')}")
                    print(f"    Prix: {trip.get('price_simple')} / {trip.get('price_return')} FCFA")
                    print(f"    Places: {trip.get('available_seats')}/{trip.get('max_seats')}")
                
                return True
            else:
                print(f"❌ API retourne une erreur: {json_data.get('message')}")
                return False
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous qu'il fonctionne sur http://127.0.0.1:8009")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout de la requête")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_database_trips():
    """Test direct de la base de données"""
    print("\n🔍 Test direct de la base de données")
    
    try:
        from travel.models import Trip, Booking
        
        # Compter les voyages
        trips_count = Trip.objects.count()
        print(f"Voyages en base: {trips_count}")
        
        if trips_count > 0:
            # Afficher quelques voyages
            for trip in Trip.objects.all()[:3]:
                print(f"  - ID {trip.id}: {trip.departure_city} → {trip.arrival_city}")
                print(f"    Date: {trip.date}, Prix: {trip.price_simple}/{trip.price_return}")
                print(f"    Max places: {trip.max_seats}")
                
                # Vérifier les réservations
                bookings = Booking.objects.filter(trip=trip)
                print(f"    Réservations: {bookings.count()}")
        
        return trips_count > 0
        
    except Exception as e:
        print(f"❌ Erreur base de données: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'API des voyages")
    print("=" * 40)
    
    # Test 1: Base de données
    if not test_database_trips():
        print("❌ Problème avec la base de données")
        sys.exit(1)
    
    # Test 2: API
    if not test_api_direct():
        print("❌ Problème avec l'API")
        sys.exit(1)
    
    print("\n✅ Tous les tests ont réussi!")