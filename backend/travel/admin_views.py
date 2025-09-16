from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Trip, Bus, CustomUser
import json

def admin_dashboard(request):
    """Vue principale du dashboard admin"""
    context = {
        'page_title': 'Dashboard Admin',
        'total_trips': Trip.objects.count(),
        'total_buses': Bus.objects.count(),
        'total_users': CustomUser.objects.count(),
        'total_bookings': 0,  # À implémenter avec le modèle Booking
    }
    return render(request, 'admin/dashboard.html', context)

def admin_trips_list(request):
    """Liste tous les voyages avec interface simple"""
    trips = Trip.objects.select_related('bus').all().order_by('-created_at')
    context = {
        'page_title': 'Gestion des Voyages',
        'trips': trips,
    }
    return render(request, 'admin/trips_list.html', context)

def admin_buses_list(request):
    """Liste tous les bus avec interface simple"""
    buses = Bus.objects.all().order_by('bus_number')
    context = {
        'page_title': 'Gestion des Autobus',
        'buses': buses,
    }
    return render(request, 'admin/buses_list.html', context)

def admin_bus_delete(request, bus_id):
    """Supprime un bus"""
    bus = get_object_or_404(Bus, id=bus_id)
    
    if request.method == 'POST':
        bus_number = bus.bus_number
        bus.delete()
        messages.success(request, f'Bus {bus_number} supprimé avec succès!')
        return redirect('admin_buses_list')
    
    context = {
        'page_title': 'Supprimer Bus',
        'bus': bus,
    }
    return render(request, 'admin/bus_delete.html', context)

def admin_bus_edit(request, bus_id):
    """Modifie un bus"""
    bus = get_object_or_404(Bus, id=bus_id)
    
    if request.method == 'POST':
        bus.bus_number = request.POST.get('bus_number', bus.bus_number)
        bus.bus_model = request.POST.get('bus_model', bus.bus_model)
        bus.total_seats = request.POST.get('total_seats', bus.total_seats)
        year_value = request.POST.get('year')
        bus.year = int(year_value) if year_value else None
        bus.status = request.POST.get('status', bus.status)
        bus.save()
        
        messages.success(request, f'Bus {bus.bus_number} modifié avec succès!')
        return redirect('admin_buses_list')
    
    context = {
        'page_title': 'Modifier Bus',
        'bus': bus,
    }
    return render(request, 'admin/bus_edit.html', context)

def admin_bus_create(request):
    """Crée un nouveau bus"""
    if request.method == 'POST':
        bus = Bus(
            bus_number=request.POST.get('bus_number'),
            bus_model=request.POST.get('bus_model'),
            total_seats=request.POST.get('total_seats'),
            year=request.POST.get('year') if request.POST.get('year') else None,
            status=request.POST.get('status', 'disponible')
        )
        bus.save()
        
        messages.success(request, f'Bus {bus.bus_number} créé avec succès!')
        return redirect('admin_buses_list')
    
    context = {
        'page_title': 'Nouveau Bus',
    }
    return render(request, 'admin/bus_create.html', context)

# Gestion des voyages
def admin_trips_list(request):
    """Liste tous les voyages avec interface simple"""
    trips = Trip.objects.select_related('bus').all().order_by('-date', '-departure_time')
    context = {
        'page_title': 'Gestion des Voyages',
        'trips': trips,
    }
    return render(request, 'admin/trips_list.html', context)

def admin_trip_create(request):
    """Crée un nouveau voyage"""
    if request.method == 'POST':
        trip = Trip(
            trip_number=request.POST.get('trip_number'),
            departure_city=request.POST.get('departure_city'),
            arrival_city=request.POST.get('arrival_city'),
            date=request.POST.get('departure_date'),
            departure_time=request.POST.get('departure_time'),
            price_simple=request.POST.get('price_simple'),
            price_round_trip=request.POST.get('price_round_trip', '0'),
            status=request.POST.get('status', 'programmed')
        )
        
        # Assigner un bus si spécifié
        bus_id = request.POST.get('bus_id')
        if bus_id:
            try:
                trip.bus = Bus.objects.get(id=bus_id)
            except Bus.DoesNotExist:
                pass
        
        trip.save()
        messages.success(request, f'Voyage {trip.trip_number} créé avec succès!')
        return redirect('admin_trips_list')
    
    buses = Bus.objects.filter(status='disponible').order_by('bus_number')
    context = {
        'page_title': 'Nouveau Voyage',
        'buses': buses,
    }
    return render(request, 'admin/trip_create.html', context)

def admin_trip_edit(request, trip_id):
    """Modifie un voyage"""
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        trip.trip_number = request.POST.get('trip_number', trip.trip_number)
        trip.departure_city = request.POST.get('departure_city', trip.departure_city)
        trip.arrival_city = request.POST.get('arrival_city', trip.arrival_city)
        trip.date = request.POST.get('departure_date', trip.date)
        trip.departure_time = request.POST.get('departure_time', trip.departure_time)
        trip.price_simple = request.POST.get('price_simple', trip.price_simple)
        trip.price_round_trip = request.POST.get('price_round_trip', trip.price_round_trip)
        trip.status = request.POST.get('status', trip.status)
        
        # Assigner un bus si spécifié
        bus_id = request.POST.get('bus_id')
        if bus_id:
            try:
                trip.bus = Bus.objects.get(id=bus_id)
            except Bus.DoesNotExist:
                trip.bus = None
        else:
            trip.bus = None
        
        trip.save()
        messages.success(request, f'Voyage {trip.trip_number} modifié avec succès!')
        return redirect('admin_trips_list')
    
    buses = Bus.objects.filter(status='disponible').order_by('bus_number')
    context = {
        'page_title': 'Modifier Voyage',
        'trip': trip,
        'buses': buses,
    }
    return render(request, 'admin/trip_edit.html', context)

def admin_trip_delete(request, trip_id):
    """Supprime un voyage"""
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        trip_number = trip.trip_number
        trip.delete()
        messages.success(request, f'Voyage {trip_number} supprimé avec succès!')
        return redirect('admin_trips_list')
    
    context = {
        'page_title': 'Supprimer Voyage',
        'trip': trip,
    }
    return render(request, 'admin/trip_delete.html', context)

# Gestion des chauffeurs
def admin_drivers_list(request):
    """Liste tous les chauffeurs avec interface simple"""
    drivers = CustomUser.objects.filter(role='driver').order_by('username')
    context = {
        'page_title': 'Gestion des Chauffeurs',
        'drivers': drivers,
    }
    return render(request, 'admin/drivers_list.html', context)

def admin_driver_create(request):
    """Crée un nouveau chauffeur"""
    if request.method == 'POST':
        driver = CustomUser(
            username=request.POST.get('username'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            license_number=request.POST.get('license_number'),
            experience_years=int(request.POST.get('experience_years', 0)),
            role='driver',
            is_available=True
        )
        driver.set_password(request.POST.get('password', 'chauffeur123'))
        driver.save()
        
        messages.success(request, f'Chauffeur {driver.first_name} {driver.last_name} créé avec succès!')
        return redirect('admin_drivers_list')
    
    context = {
        'page_title': 'Nouveau Chauffeur',
    }
    return render(request, 'admin/driver_create.html', context)

def admin_driver_edit(request, driver_id):
    """Modifie un chauffeur"""
    driver = get_object_or_404(CustomUser, id=driver_id, role='driver')
    
    if request.method == 'POST':
        driver.username = request.POST.get('username', driver.username)
        driver.first_name = request.POST.get('first_name', driver.first_name)
        driver.last_name = request.POST.get('last_name', driver.last_name)
        driver.email = request.POST.get('email', driver.email)
        driver.phone = request.POST.get('phone', driver.phone)
        driver.license_number = request.POST.get('license_number', driver.license_number)
        driver.experience_years = int(request.POST.get('experience_years', driver.experience_years))
        driver.is_available = request.POST.get('is_available') == 'on'
        
        # Changer le mot de passe seulement si fourni
        new_password = request.POST.get('password')
        if new_password:
            driver.set_password(new_password)
        
        driver.save()
        messages.success(request, f'Chauffeur {driver.first_name} {driver.last_name} modifié avec succès!')
        return redirect('admin_drivers_list')
    
    context = {
        'page_title': 'Modifier Chauffeur',
        'driver': driver,
    }
    return render(request, 'admin/driver_edit.html', context)

def admin_driver_delete(request, driver_id):
    """Supprime un chauffeur"""
    driver = get_object_or_404(CustomUser, id=driver_id, role='driver')
    
    if request.method == 'POST':
        driver_name = f"{driver.first_name} {driver.last_name}"
        driver.delete()
        messages.success(request, f'Chauffeur {driver_name} supprimé avec succès!')
        return redirect('admin_drivers_list')
    
    context = {
        'page_title': 'Supprimer Chauffeur',
        'driver': driver,
    }
    return render(request, 'admin/driver_delete.html', context)