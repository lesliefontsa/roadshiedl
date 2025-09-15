from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Bus, CustomUser, Trip
from alerts.models import Alert
from django.shortcuts import get_object_or_404

def staff_required(view):
    # Temporairement désactivé pour permettre l'accès via frontend auth
    return view
    # return user_passes_test(lambda u: u.is_active and u.is_staff)(view)


@staff_required
def backoffice_buses(request):
    # Handle create / edit
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        bus_number = request.POST.get('bus_number')
        bus_model = request.POST.get('bus_model')
        total_seats = request.POST.get('total_seats')
        status = request.POST.get('status')
        if edit_id:
            b = get_object_or_404(Bus, id=edit_id)
            b.bus_number = bus_number
            b.bus_model = bus_model
            b.total_seats = int(total_seats)
            b.status = status
            b.save()
            return redirect('travel:backoffice_buses')
        else:
            Bus.objects.create(bus_number=bus_number, bus_model=bus_model, total_seats=int(total_seats), status=status)
            return redirect('travel:backoffice_buses')

    # Support editing via query param ?edit=<id>
    edit_bus = None
    if 'edit' in request.GET:
        edit_bus = get_object_or_404(Bus, id=request.GET.get('edit'))

    buses = Bus.objects.all()
    return render(request, 'backoffice/buses.html', {'buses': buses, 'title': 'Buses', 'edit_bus': edit_bus})


@staff_required
def backoffice_bus_delete(request, bus_id):
    b = get_object_or_404(Bus, id=bus_id)
    b.delete()
    return redirect('travel:backoffice_buses')


@staff_required
def backoffice_trips(request):
    """Gestion des voyages avec prix en FCFA"""
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        trip_number = request.POST.get('trip_number')
        departure_city = request.POST.get('departure_city')
        arrival_city = request.POST.get('arrival_city')
        date = request.POST.get('date')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        bus_id = request.POST.get('bus_id')
        driver_id = request.POST.get('driver_id')
        price_simple = request.POST.get('price_simple')
        price_return = request.POST.get('price_return')
        max_seats = request.POST.get('max_seats')
        notes = request.POST.get('notes')
        
        if edit_id:
            # Modifier un voyage existant
            trip = get_object_or_404(Trip, id=edit_id)
            trip.trip_number = trip_number
            trip.departure_city = departure_city
            trip.arrival_city = arrival_city
            trip.date = date
            trip.departure_time = departure_time
            trip.arrival_time = arrival_time
            trip.bus_id = bus_id
            trip.driver_id = driver_id if driver_id else None
            trip.price_simple = price_simple
            trip.price_return = price_return
            trip.max_seats = max_seats
            trip.notes = notes
            trip.save()
            return redirect('travel:backoffice_trips')
        else:
            # Créer un nouveau voyage
            # Récupérer l'utilisateur créateur (admin connecté)
            created_by = request.user if request.user.is_authenticated else CustomUser.objects.filter(is_staff=True).first()
            
            Trip.objects.create(
                trip_number=trip_number,
                departure_city=departure_city,
                arrival_city=arrival_city,
                date=date,
                departure_time=departure_time,
                arrival_time=arrival_time,
                bus_id=bus_id,
                driver_id=driver_id if driver_id else None,
                price_simple=price_simple,
                price_return=price_return,
                max_seats=max_seats,
                notes=notes,
                created_by=created_by
            )
            return redirect('travel:backoffice_trips')
    
    # Support pour édition via query param ?edit=<id>
    edit_trip = None
    if 'edit' in request.GET:
        edit_trip = get_object_or_404(Trip, id=request.GET.get('edit'))
    
    # Récupérer les données nécessaires pour les formulaires
    trips = Trip.objects.all().order_by('-date')
    buses = Bus.objects.filter(status='disponible')
    drivers = CustomUser.objects.filter(role='driver', is_available=True)
    
    # Statistiques
    total_trips = trips.count()
    active_trips = trips.filter(status__in=['programmed', 'boarding', 'in_transit']).count()
    completed_trips = trips.filter(status='completed').count()
    avg_price_simple = trips.aggregate(models.Avg('price_simple'))['price_simple__avg'] or 0
    
    context = {
        'trips': trips,
        'buses': buses,
        'drivers': drivers,
        'edit_trip': edit_trip,
        'title': 'Voyages',
        'total_trips': total_trips,
        'active_trips': active_trips,
        'completed_trips': completed_trips,
        'avg_price_simple': avg_price_simple,
    }
    
    return render(request, 'backoffice/trips.html', context)


@staff_required
def backoffice_trip_delete(request, trip_id):
    """Supprimer un voyage"""
    trip = get_object_or_404(Trip, id=trip_id)
    trip.delete()
    return redirect('travel:backoffice_trips')


@staff_required
def backoffice_drivers(request):
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rating = request.POST.get('rating')
        license_number = request.POST.get('license_number')
        phone = request.POST.get('phone')
        
        if edit_id:
            # Modification d'un chauffeur existant
            driver = get_object_or_404(CustomUser, id=edit_id, role='driver')
            driver.username = username
            driver.email = email
            driver.first_name = first_name or ''
            driver.last_name = last_name or ''
            driver.phone = phone or ''
            driver.license_number = license_number or ''
            if rating:
                try:
                    driver.rating = float(rating)
                except ValueError:
                    driver.rating = 0.0
            driver.save()
            return redirect('travel:backoffice_drivers')
        else:
            # Création d'un nouveau chauffeur
            password = request.POST.get('password')
            if not password:
                password = 'temp123'  # Mot de passe temporaire par défaut
            
            driver = CustomUser.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name or '',
                last_name=last_name or ''
            )
            driver.role = 'driver'
            driver.is_staff = True
            driver.phone = phone or ''
            driver.license_number = license_number or ''
            if rating:
                try:
                    driver.rating = float(rating)
                except ValueError:
                    driver.rating = 0.0
            driver.save()
            return redirect('travel:backoffice_drivers')

    # Support editing via query param ?edit=<id>
    edit_driver = None
    if 'edit' in request.GET:
        edit_driver = get_object_or_404(CustomUser, id=request.GET.get('edit'), role='driver')

    drivers = CustomUser.objects.filter(role='driver')
    return render(request, 'backoffice/drivers.html', {
        'drivers': drivers, 
        'title': 'Drivers', 
        'edit_driver': edit_driver
    })


@staff_required
def backoffice_trips(request):
    if request.method == 'POST':
        departure_city = request.POST.get('departure_city')
        arrival_city = request.POST.get('arrival_city')
        date = request.POST.get('date')
        departure_time = request.POST.get('departure_time')
        bus_id = request.POST.get('bus_id')
        bus = Bus.objects.get(id=bus_id)
        Trip.objects.create(departure_city=departure_city, arrival_city=arrival_city, date=date, departure_time=departure_time, bus=bus, price_simple=0, price_return=0, created_by=request.user)
        return redirect('travel:backoffice_trips')

    buses = Bus.objects.all()
    trips = Trip.objects.all()
    return render(request, 'backoffice/trips.html', {'buses': buses, 'trips': trips, 'title': 'Trips'})


@staff_required
def backoffice_alerts(request):
    if request.method == 'POST':
        handle_id = request.POST.get('handle_id')
        if handle_id:
            a = Alert.objects.filter(id=handle_id).first()
            if a:
                a.status = 'resolved'
                a.save()
        return redirect('travel:backoffice_alerts')

    alerts = Alert.objects.order_by('-created_at')[:200]
    return render(request, 'backoffice/alerts.html', {'alerts': alerts, 'title': 'Alerts'})
