from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from travel.models import CustomUser, Bus, Trip, Booking, SomnolenceAlert
import random

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new sample data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            SomnolenceAlert.objects.all().delete()
            Booking.objects.all().delete()
            Trip.objects.all().delete()
            Bus.objects.all().delete()
            CustomUser.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create drivers
        drivers_data = [
            {'username': 'driver1', 'first_name': 'Jean', 'last_name': 'Dupont', 'email': 'jean.dupont@roadshield.com', 'license_number': 'DRV001', 'experience_years': 5},
            {'username': 'driver2', 'first_name': 'Marie', 'last_name': 'Martin', 'email': 'marie.martin@roadshield.com', 'license_number': 'DRV002', 'experience_years': 8},
            {'username': 'driver3', 'first_name': 'Paul', 'last_name': 'Bernard', 'email': 'paul.bernard@roadshield.com', 'license_number': 'DRV003', 'experience_years': 3},
        ]
        
        for driver_data in drivers_data:
            driver, created = CustomUser.objects.get_or_create(
                username=driver_data['username'],
                defaults={
                    'first_name': driver_data['first_name'],
                    'last_name': driver_data['last_name'],
                    'email': driver_data['email'],
                    'role': 'driver',
                    'license_number': driver_data['license_number'],
                    'experience_years': driver_data['experience_years'],
                    'rating': random.uniform(3.5, 5.0),
                    'is_available': True,
                    'phone': f'+221 77 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}',
                    'address': f'{random.randint(1, 100)} Avenue de la République, Dakar'
                }
            )
            if created:
                driver.set_password('password123')
                driver.save()
                self.stdout.write(f'Created driver: {driver.get_full_name()}')
        
        # Create buses
        buses_data = [
            {'bus_number': 'BUS001', 'bus_model': 'Mercedes Sprinter', 'total_seats': 25, 'year': 2022},
            {'bus_number': 'BUS002', 'bus_model': 'Iveco Daily', 'total_seats': 30, 'year': 2021},
            {'bus_number': 'BUS003', 'bus_model': 'Volkswagen Crafter', 'total_seats': 20, 'year': 2023},
            {'bus_number': 'BUS004', 'bus_model': 'Ford Transit', 'total_seats': 15, 'year': 2020},
        ]
        
        drivers = list(CustomUser.objects.filter(role='driver'))
        
        for i, bus_data in enumerate(buses_data):
            bus, created = Bus.objects.get_or_create(
                bus_number=bus_data['bus_number'],
                defaults={
                    'bus_model': bus_data['bus_model'],
                    'total_seats': bus_data['total_seats'],
                    'year': bus_data['year'],
                    'status': 'disponible',
                    'mileage': random.randint(10000, 150000),
                    'assigned_driver': drivers[i % len(drivers)] if drivers else None,
                    'arduino_device_id': f'ARD{bus_data["bus_number"][-3:]}'
                }
            )
            if created:
                self.stdout.write(f'Created bus: {bus.bus_number} - {bus.bus_model}')
        
        # Create clients
        clients_data = [
            {'username': 'client1', 'first_name': 'Fatou', 'last_name': 'Diop', 'email': 'fatou.diop@email.com'},
            {'username': 'client2', 'first_name': 'Amadou', 'last_name': 'Sy', 'email': 'amadou.sy@email.com'},
            {'username': 'client3', 'first_name': 'Aïssatou', 'last_name': 'Fall', 'email': 'aissatou.fall@email.com'},
        ]
        
        for client_data in clients_data:
            client, created = CustomUser.objects.get_or_create(
                username=client_data['username'],
                defaults={
                    'first_name': client_data['first_name'],
                    'last_name': client_data['last_name'],
                    'email': client_data['email'],
                    'role': 'client',
                    'phone': f'+221 70 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}',
                }
            )
            if created:
                client.set_password('password123')
                client.save()
                self.stdout.write(f'Created client: {client.get_full_name()}')
        
        # Create trips
        buses = list(Bus.objects.all())
        cities = [
            ('Dakar', 'Saint-Louis'),
            ('Dakar', 'Kaolack'),
            ('Dakar', 'Ziguinchor'),
            ('Saint-Louis', 'Louga'),
            ('Kaolack', 'Fatick'),
        ]
        
        admin_user = CustomUser.objects.filter(is_superuser=True).first()
        
        for i in range(10):  # Create 10 trips
            departure, arrival = random.choice(cities)
            bus = random.choice(buses)
            
            # Create trips for the next 30 days
            trip_date = timezone.now().date() + timedelta(days=random.randint(0, 30))
            departure_time = datetime.strptime(f'{random.randint(6, 22)}:{random.choice(["00", "30"])}', '%H:%M').time()
            
            trip_data = {
                'trip_type': random.choice(['one_way', 'round_trip']),
                'status': random.choice(['programmed', 'programmed', 'programmed', 'boarding']),
                'price_simple': random.randint(5000, 25000),
                'price_return': random.randint(8000, 40000),
                'driver': bus.assigned_driver,
                'created_by': admin_user,
                'notes': f'Voyage {departure} → {arrival}',
                'duration': f'{random.randint(2, 8)}h{random.choice(["00", "30"])}'
            }
            
            # Don't use get_or_create for trips since trip_number causes conflicts
            trip = Trip(
                departure_city=departure,
                arrival_city=arrival,
                date=trip_date,
                departure_time=departure_time,
                bus=bus,
                **trip_data
            )
            trip.save()  # This will auto-generate the trip_number
            self.stdout.write(f'Created trip: {trip}')
        
        # Create some bookings
        trips = Trip.objects.filter(date__gte=timezone.now().date())[:5]
        clients = list(CustomUser.objects.filter(role='client'))
        
        for trip in trips:
            for _ in range(random.randint(1, 3)):  # 1-3 bookings per trip
                client = random.choice(clients)
                seats = random.randint(1, 3)
                
                booking = Booking.objects.create(
                    trip=trip,
                    client=client,
                    passenger_name=client.get_full_name(),
                    passenger_phone=client.phone or '+221 77 000 00 00',
                    client_email=client.email,
                    seats=seats,
                    trip_type=random.choice(['aller', 'retour']),
                    unit_price=trip.price_simple,
                    total_price=trip.price_simple * seats,
                    status=random.choice(['pending', 'confirmed', 'paid']),
                    payment_method=random.choice(['orange_money', 'wave', 'cash'])
                )
                
                # Simulate some payments
                if booking.status in ['confirmed', 'paid']:
                    booking.amount_paid = booking.total_price
                elif booking.status == 'pending':
                    booking.amount_paid = random.uniform(0, booking.total_price)
                
                booking.save()
                self.stdout.write(f'Created booking: {booking.booking_reference}')
        
        # Create some drowsiness alerts
        trips_with_drivers = Trip.objects.filter(driver__isnull=False, date=timezone.now().date())
        
        for trip in trips_with_drivers[:3]:  # Create alerts for 3 trips
            alert = SomnolenceAlert.objects.create(
                bus=trip.bus,
                driver=trip.driver,
                trip=trip,
                duration_seconds=random.uniform(1.5, 6.0),
                severity=random.choice(['low', 'medium', 'high', 'critical']),
                arduino_device_id=trip.bus.arduino_device_id,
                sensor_confidence=random.uniform(0.7, 1.0),
                raw_data={'eyes_closed_duration': random.uniform(1.5, 6.0), 'confidence': random.uniform(0.7, 1.0)},
                notes=f'Alerte détectée pendant le voyage {trip.departure_city} → {trip.arrival_city}'
            )
            self.stdout.write(f'Created alert: {alert.alert_id}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('You can now log in with:')
        self.stdout.write('  Admin: admin / [your password]')
        self.stdout.write('  Drivers: driver1, driver2, driver3 / password123')
        self.stdout.write('  Clients: client1, client2, client3 / password123')