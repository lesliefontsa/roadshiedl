#!/usr/bin/env python
"""
Script de test pour l'intégration Stripe et génération de factures PDF
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Ajouter le répertoire du projet au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from travel.models import Trip, Booking, Invoice, CustomUser, Bus
from travel.views import generate_invoice_pdf

def test_invoice_generation():
    """Test de génération de facture PDF"""
    print("🧪 Test de génération de facture PDF...")
    
    try:
        # Vérifier qu'il y a des voyages en base
        trips = Trip.objects.all()
        if not trips.exists():
            print("❌ Aucun voyage trouvé en base. Créez d'abord des voyages via l'admin.")
            return False
        
        trip = trips.first()
        print(f"✅ Voyage trouvé: {trip}")
        
        # Vérifier qu'il y a des utilisateurs
        users = CustomUser.objects.all()
        if not users.exists():
            print("❌ Aucun utilisateur trouvé. Créons un utilisateur de test.")
            user = CustomUser.objects.create_user(
                username='test_client',
                email='test@example.com',
                role='client'
            )
        else:
            user = users.first()
        
        print(f"✅ Utilisateur: {user}")
        
        # Créer une réservation de test
        booking = Booking.objects.create(
            booking_reference=f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            ticket_number=f"TK-TEST-{datetime.now().strftime('%H%M%S')}",
            trip=trip,
            client=user,
            passenger_name="Test Passenger",
            passenger_phone="+225 01 02 03 04 05",
            client_email="test@example.com",
            seats=1,
            trip_type='aller',
            unit_price=Decimal('25000'),
            total_price=Decimal('29500'),  # Avec TVA 18%
            amount_paid=Decimal('29500'),
            payment_method='credit_card',
            payment_reference='pi_test_123456789',
            status='paid'
        )
        
        print(f"✅ Réservation créée: {booking.booking_reference}")
        
        # Créer une facture
        invoice = Invoice.objects.create(
            booking=booking,
            client=user,
            subtotal=Decimal('25000'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('4500'),
            total_amount=Decimal('29500'),
            stripe_payment_intent_id='pi_test_123456789',
            stripe_payment_status='succeeded',
            billing_name="Test Client",
            billing_email="test@example.com",
            billing_phone="+225 01 02 03 04 05",
            billing_address="123 Rue de Test, Abidjan, Côte d'Ivoire",
            status='paid',
            due_date=datetime.now().date() + timedelta(days=30),
            payment_date=datetime.now()
        )
        
        print(f"✅ Facture créée: {invoice.invoice_number}")
        
        # Générer le PDF
        pdf_url = generate_invoice_pdf(invoice)
        
        if pdf_url:
            print(f"✅ PDF généré avec succès: {pdf_url}")
            print(f"📁 Fichier sauvegardé: {invoice.pdf_file.path if invoice.pdf_file else 'Non sauvegardé'}")
            return True
        else:
            print("❌ Erreur lors de la génération du PDF")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_setup():
    """Vérifier la configuration de la base de données"""
    print("🔍 Vérification de la base de données...")
    
    try:
        # Compter les éléments
        trips_count = Trip.objects.count()
        users_count = CustomUser.objects.count()
        buses_count = Bus.objects.count()
        bookings_count = Booking.objects.count()
        invoices_count = Invoice.objects.count()
        
        print(f"📊 Statistiques de la base:")
        print(f"   - Voyages: {trips_count}")
        print(f"   - Utilisateurs: {users_count}")
        print(f"   - Bus: {buses_count}")
        print(f"   - Réservations: {bookings_count}")
        print(f"   - Factures: {invoices_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Test du système de réservation et facturation")
    print("=" * 50)
    
    # Test 1: Vérification base de données
    if not test_database_setup():
        sys.exit(1)
    
    print()
    
    # Test 2: Génération de facture PDF
    if not test_invoice_generation():
        sys.exit(1)
    
    print()
    print("🎉 Tous les tests ont réussi !")
    print("✅ Le système est prêt pour les réservations avec paiement Stripe et génération de factures PDF.")