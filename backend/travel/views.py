# travel/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from django.conf import settings
from .models import CustomUser, Bus, Trip, Booking
from .models import SomnolenceAlert
from django.db import transaction
import json
import jwt
import time
from decimal import Decimal
from datetime import datetime

def client_dashboard_view(request):
    """Vue pour le dashboard client"""
    return render(request, 'client-dashboard.html')

@csrf_exempt
def api_login_view(request):
    """API d'authentification ultra-simple"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)
    
    # Support multiformat
    username = None
    password = None
    
    try:
        if request.body and 'application/json' in str(request.content_type):
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
    except:
        pass
    
    if not username or not password:
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
    
    if not username or not password:
        return JsonResponse({'status': 'error', 'message': 'Username et password requis'}, status=400)
    
    # Vérification simple des comptes hardcodés pour la présentation
    if (username == 'admin' and password == 'admin123') or (username == 'client' and password == 'client123'):
        return JsonResponse({
            'status': 'success',
            'message': 'Connexion réussie',
            'token': f'token_{username}',
            'user': {
                'username': username,
                'role': 'admin' if username == 'admin' else 'client',
                'is_staff': username == 'admin'
            }
        })
    
    # Essayer avec la base de données
    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'Connexion réussie',
                'token': f'token_{user.id}_{user.username}',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': getattr(user, 'role', 'client'),
                    'is_staff': user.is_staff
                }
            })
    except Exception as e:
        pass
    
    return JsonResponse({
        'status': 'error',
        'message': 'Nom d\'utilisateur ou mot de passe incorrect.'
    }, status=400)

@csrf_exempt
def login_view(request):
    """Page de connexion avec authentification Django et API JSON"""
    if request.user.is_authenticated:
        # Rediriger selon si l'utilisateur est staff (admin) ou client
        if request.user.is_staff:
            return redirect('/admin-backoffice/')
        else:
            return redirect('/client-dashboard/')
    
    if request.method == 'POST':
        # Check if it's JSON data (API request) or form data
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            is_api_request = True
        except:
            username = request.POST.get('username')
            password = request.POST.get('password')
            is_api_request = False
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if is_api_request:
                # Return JSON response for API requests
                return JsonResponse({
                    'status': 'success',
                    'message': 'Connexion réussie',
                    'token': f'token_{user.id}_{user.username}',  # Simple token for demo
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': 'admin' if user.is_staff else 'client',
                        'is_staff': user.is_staff
                    }
                })
            else:
                # Traditional redirect for form submission
                if user.is_staff:
                    return redirect('/admin-backoffice/')
                else:
                    return redirect('/client-dashboard/')
        else:
            if is_api_request:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Nom d\'utilisateur ou mot de passe incorrect.'
                }, status=400)
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    """Déconnexion"""
    logout(request)
    return redirect('/auth/login/')

@csrf_exempt
def register_view(request):
    """Inscription d'un nouveau client avec support API JSON"""
    if request.method == 'POST':
        # Check if it's JSON data (API request) or form data
        try:
            data = json.loads(request.body)
            is_api_request = True
        except:
            data = request.POST
            is_api_request = False
        
        # Extract data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        phone = data.get('phone', '')
        
        # Validation
        if not all([username, email, password]):
            error_msg = 'Nom d\'utilisateur, email et mot de passe sont requis.'
            if is_api_request:
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            else:
                messages.error(request, error_msg)
                return render(request, 'auth/register.html')
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            error_msg = 'Ce nom d\'utilisateur existe déjà.'
            if is_api_request:
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            else:
                messages.error(request, error_msg)
                return render(request, 'auth/register.html')
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            error_msg = 'Cet email est déjà utilisé.'
            if is_api_request:
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            else:
                messages.error(request, error_msg)
                return render(request, 'auth/register.html')
        
        try:
            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role='client'
            )
            
            # Automatically log in the user
            login(request, user)
            
            if is_api_request:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Compte créé avec succès',
                    'token': f'token_{user.id}_{user.username}',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': 'client',
                        'is_staff': False
                    }
                })
            else:
                messages.success(request, 'Compte créé avec succès !')
                return redirect('/client-dashboard/')
                
        except Exception as e:
            error_msg = f'Erreur lors de la création du compte: {str(e)}'
            if is_api_request:
                return JsonResponse({'status': 'error', 'message': error_msg}, status=500)
            else:
                messages.error(request, error_msg)
                return render(request, 'auth/register.html')
    
    return render(request, 'auth/register.html')

def admin_dashboard(request):
    """Dashboard administrateur avec données réelles"""
    # Vérification optionnelle du staff (temporaire pour test frontend)
    # if not request.user.is_authenticated or not request.user.is_staff:
    #     return redirect('/auth/login/')
    
    # Statistiques
    total_trips = Trip.objects.count()
    total_bookings = Booking.objects.filter(status__in=['confirmed', 'validated']).count()
    total_revenue = Booking.objects.filter(
        status__in=['confirmed', 'validated']
    ).aggregate(total=models.Sum('total_price'))['total'] or Decimal('0')
    available_buses = Bus.objects.filter(status='disponible').count()
    
    # Utiliser des données par défaut si pas d'utilisateur connecté
    user_display = request.user if request.user.is_authenticated else type('obj', (object,), {
        'first_name': 'Admin', 'last_name': 'Demo', 'username': 'demo'
    })()
    
    context = {
        'user': user_display,
        'total_trips': total_trips,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'available_buses': available_buses,
        'recent_bookings': Booking.objects.order_by('-booking_date')[:10],
    }
    
    return render(request, 'admin/dashboard.html', context)

def admin_backoffice(request):
    """Back-office administrateur avec gestion complète"""
    # Optionnel: vérification d'authentification
    # if not request.user.is_authenticated or not request.user.is_staff:
    #     return redirect('/auth/login/')
    
    # Données pour le back-office (similaire au dashboard mais plus détaillé)
    total_trips = Trip.objects.count()
    total_bookings = Booking.objects.filter(status__in=['confirmed', 'validated']).count()
    total_revenue = Booking.objects.filter(
        status__in=['confirmed', 'validated']
    ).aggregate(total=models.Sum('total_price'))['total'] or Decimal('0')
    available_buses = Bus.objects.filter(status='disponible').count()
    total_drivers = CustomUser.objects.filter(role='driver').count()
    
    # Utilisateur actuel ou données de démo
    user_display = request.user if request.user.is_authenticated else type('obj', (object,), {
        'first_name': 'Admin', 'last_name': 'Backoffice', 'username': 'admin'
    })()
    
    context = {
        'user': user_display,
        'total_trips': total_trips,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'available_buses': available_buses,
        'total_drivers': total_drivers,
        'recent_bookings': Booking.objects.order_by('-booking_date')[:10],
    }
    
    return render(request, 'admin-backoffice.html', context)

def client_dashboard(request):
    """Dashboard client avec ses réservations"""
    # Vérification optionnelle (temporaire pour test frontend)
    # if not request.user.is_authenticated:
    #     return redirect('/auth/login/')
    
    # Voyages disponibles
    available_trips = Trip.objects.filter(
        date__gte=datetime.now().date()
    ).order_by('date', 'departure_time')
    
    # Réservations du client (vide si pas connecté)
    my_bookings = Booking.objects.filter(
        client=request.user
    ).order_by('-booking_date') if request.user.is_authenticated else []
    
    # Utiliser des données par défaut si pas d'utilisateur connecté
    user_display = request.user if request.user.is_authenticated else type('obj', (object,), {
        'first_name': 'Client', 'last_name': 'Demo', 'username': 'demo', 'email': 'demo@example.com',
        'phone': '+237 6XX XXX XXX', 'date_joined': datetime.now()
    })()
    
    context = {
        'user': user_display,
        'available_trips': available_trips,
        'my_bookings': my_bookings,
    }
    
    return render(request, 'client-dashboard.html', context)

@csrf_exempt
@login_required
def api_trips(request):
    """API pour récupérer les voyages"""
    if request.method == 'GET':
        trips = Trip.objects.filter(date__gte=datetime.now().date())
        trips_data = []
        
        for trip in trips:
            trips_data.append({
                'id': trip.id,
                'departure_city': trip.departure_city,
                'arrival_city': trip.arrival_city,
                'date': trip.date.isoformat(),
                'departure_time': trip.departure_time.strftime('%H:%M'),
                'duration': trip.duration,
                'bus_id': trip.bus.bus_number,
                'price_simple': float(trip.price_simple),
                'price_return': float(trip.price_return),
                'available_seats': trip.available_seats,
                'notes': trip.notes,
            })
        
        return JsonResponse({'trips': trips_data})

@csrf_exempt
@login_required
@csrf_exempt
def api_create_booking(request):
    """API pour créer une réservation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Vérifier si l'utilisateur est connecté (pour les clients authentifiés)
            if not request.user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'Utilisateur non connecté'})
            
            trip = Trip.objects.get(id=data['trip_id'])
            
            # Créer une réservation simplifiée pour client connecté
            booking = Booking.objects.create(
                trip=trip,
                client=request.user,
                client_email=request.user.email,
                seats=1,  # Par défaut 1 place
                trip_type=data.get('trip_type', 'one_way'),
                total_price=Decimal(str(data['total_price'])),
                status='confirmed',  # Confirmation automatique pour les clients connectés
                ticket_number=f"RD{datetime.now().strftime('%y%m%d%H%M%S')}{trip.id}"
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Réservation créée avec succès',
                'booking_id': booking.id,
                'ticket_number': booking.ticket_number
            })
            
        except Trip.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Voyage non trouvé'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

# Middleware pour forcer l'authentification
class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # URLs qui ne nécessitent pas d'authentification
        exempt_urls = ['/auth/login/', '/auth/logout/', '/admin/']
        
        # Vérifier si l'URL nécessite une authentification
        if not any(request.path.startswith(url) for url in exempt_urls):
            if not request.user.is_authenticated:
                return redirect('/auth/login/')
        
        response = self.get_response(request)
        return response


@csrf_exempt
def api_arduino_alert(request):
    """Endpoint to receive Arduino somnolence alerts (no auth for now)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    try:
        payload = json.loads(request.body)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'invalid json'}, status=400)

    bus = None
    driver = None
    if 'bus_id' in payload:
        try:
            bus = Bus.objects.filter(id=payload['bus_id']).first()
        except:
            bus = None

    if 'driver_id' in payload:
        try:
            driver = CustomUser.objects.filter(id=payload['driver_id']).first()
        except:
            driver = None

    duration = float(payload.get('duration_seconds', 0))

    alert = SomnolenceAlert.objects.create(
        bus=bus,
        driver=driver,
        duration_seconds=duration,
        raw=payload
    )

    # Optionally: trigger notifications (omitted)

    return JsonResponse({'success': True, 'alert_id': alert.id})

@csrf_exempt
def create_driver_view(request):
    """API pour créer un nouveau chauffeur - SIMPLE VERSION"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode POST requise'
        }, status=405)
    
    try:
        # Accepter les données JSON OU de formulaire
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            print(f"DEBUG: Données JSON reçues: {data}")
        else:
            # Données de formulaire URL-encodées
            data = dict(request.POST)
            # Convertir les listes en valeurs simples
            for key, value in data.items():
                if isinstance(value, list) and len(value) == 1:
                    data[key] = value[0]
            print(f"DEBUG: Données POST reçues: {data}")
            
    except json.JSONDecodeError as e:
        print(f"DEBUG: Erreur JSON: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Format de données invalide'
        }, status=400)
    
    # Validation des champs requis (seulement les vrais champs requis)
    required_fields = ['username', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            return JsonResponse({
                'status': 'error',
                'message': f'Le champ {field} est requis'
            }, status=400)
    
    try:
        print(f"DEBUG: Vérification des doublons...")
        
        # Vérifier que le nom d'utilisateur n'existe pas déjà
        if CustomUser.objects.filter(username=data['username']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Ce nom d\'utilisateur existe déjà'
            }, status=400)
        
        print(f"DEBUG: Création du chauffeur...")
        
        # Générer un license_number unique
        license_number = data.get('license_number', '')
        if not license_number or CustomUser.objects.filter(license_number=license_number).exists():
            import random
            attempt = 0
            while attempt < 10:  # Max 10 tentatives
                license_number = f"LIC{random.randint(100000, 999999)}"
                if not CustomUser.objects.filter(license_number=license_number).exists():
                    break
                attempt += 1
            
            if attempt >= 10:
                license_number = f"LIC{int(time.time())}"  # Utiliser timestamp comme dernier recours
        
        # Traiter date_of_birth
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                from datetime import datetime
                date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Traiter is_available (vient sous forme de string)
        is_available = data.get('is_available', 'true').lower() == 'true'
        
        # Créer le chauffeur avec TOUS les champs
        driver = CustomUser(
            username=data['username'],
            email=data.get('email', ''),
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='driver',
            phone=data.get('phone', ''),
            date_of_birth=date_of_birth,
            license_number=license_number,
            experience_years=int(data.get('experience_years', 0)),
            rating=float(data.get('rating', 0.0)),
            total_ratings=0,
            is_available=is_available,
            address=data.get('address', '')
        )
        
        # Mot de passe simple
        driver.set_password('roadshield123')
        driver.save()
        
        print(f"DEBUG: Chauffeur créé avec ID: {driver.id}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Chauffeur {driver.first_name} {driver.last_name} créé avec succès !',
            'driver_id': driver.id,
            'driver_details': {
                'username': driver.username,
                'email': driver.email,
                'phone': driver.phone,
                'license_number': driver.license_number,
                'experience_years': driver.experience_years,
                'rating': driver.rating,
                'is_available': driver.is_available,
                'date_of_birth': str(driver.date_of_birth) if driver.date_of_birth else None
            }
        })
        
    except Exception as e:
        print(f"DEBUG: Erreur lors de la création: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur: {str(e)}'
        }, status=500)

@csrf_exempt
def create_bus_view(request):
    """API pour créer un nouveau bus"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode POST requise'
        }, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Format JSON invalide'
        }, status=400)
    
    # Validation des champs requis
    required_fields = ['bus_number', 'bus_model', 'total_seats']
    for field in required_fields:
        if not data.get(field):
            return JsonResponse({
                'status': 'error',
                'message': f'Le champ {field} est requis'
            }, status=400)
    
    try:
        # Vérifier que le numéro de bus n'existe pas déjà
        if Bus.objects.filter(bus_number=data['bus_number']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Ce numéro de bus existe déjà'
            }, status=400)
        
        # Vérifier que l'ID Arduino n'existe pas déjà (si fourni)
        arduino_id = data.get('arduino_device_id')
        if arduino_id and Bus.objects.filter(arduino_device_id=arduino_id).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Cet ID Arduino existe déjà'
            }, status=400)
        
        # Récupérer le chauffeur assigné si fourni
        assigned_driver = None
        if data.get('assigned_driver'):
            try:
                assigned_driver = CustomUser.objects.get(
                    id=data['assigned_driver'], 
                    role='driver'
                )
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Chauffeur non trouvé'
                }, status=400)
        
        # Créer le bus
        bus = Bus.objects.create(
            bus_number=data['bus_number'],
            bus_model=data['bus_model'],
            total_seats=int(data['total_seats']),
            year=int(data['year']) if data.get('year') else None,
            status=data.get('status', 'disponible'),
            mileage=int(data.get('mileage', 0)),
            assigned_driver=assigned_driver,
            arduino_device_id=arduino_id,
            notes=data.get('notes', '')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Bus créé avec succès',
            'bus_id': bus.id,
            'bus_number': bus.bus_number
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur lors de la création du bus: {str(e)}'
        }, status=500)

@csrf_exempt
def list_buses_view(request):
    """API pour lister tous les bus"""
    try:
        buses = Bus.objects.all().order_by('-created_at')
        buses_data = []
        
        for bus in buses:
            bus_data = {
                'id': bus.id,
                'bus_number': bus.bus_number,
                'bus_model': bus.bus_model,
                'total_seats': bus.total_seats,
                'year': bus.year,
                'status': bus.status,
                'mileage': bus.mileage,
                'notes': bus.notes,
                'assigned_driver': {
                    'id': bus.assigned_driver.id,
                    'name': f"{bus.assigned_driver.first_name} {bus.assigned_driver.last_name}"
                } if bus.assigned_driver else None,
                'created_at': bus.created_at.strftime('%Y-%m-%d %H:%M')
            }
            buses_data.append(bus_data)
        
        return JsonResponse({
            'status': 'success',
            'buses': buses_data,
            'total': len(buses_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur lors du chargement des bus: {str(e)}'
        }, status=500)

@csrf_exempt
def create_trip_view(request):
    """API pour créer un nouveau voyage"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode POST requise'
        }, status=405)
    
    try:
        # Traiter les données JSON ou form-data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = dict(request.POST)
            # Convertir les listes en valeurs simples
            for key, value in data.items():
                if isinstance(value, list) and len(value) == 1:
                    data[key] = value[0]
        
        print(f"DEBUG: Données voyage reçues: {data}")
        
        # Validation des champs requis
        required_fields = ['departure_city', 'arrival_city', 'date', 'departure_time', 'price_simple', 'price_return', 'bus_id']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Le champ {field} est requis'
                }, status=400)
        
        # Vérifier que le bus existe
        try:
            bus = Bus.objects.get(id=int(data['bus_id']))
        except (Bus.DoesNotExist, ValueError):
            return JsonResponse({
                'status': 'error',
                'message': 'Bus non trouvé'
            }, status=400)
        
        # Vérifier que le chauffeur existe (optionnel)
        driver = None
        if data.get('driver_id'):
            try:
                driver = CustomUser.objects.get(id=int(data['driver_id']), role='driver')
            except (CustomUser.DoesNotExist, ValueError):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Chauffeur non trouvé'
                }, status=400)
        
        # Traiter les dates
        from datetime import datetime
        try:
            departure_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            departure_time = datetime.strptime(data['departure_time'], '%H:%M').time()
            
            arrival_time = None
            if data.get('arrival_time'):
                arrival_time = datetime.strptime(data['arrival_time'], '%H:%M').time()
                
        except ValueError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Format de date/heure invalide: {str(e)}'
            }, status=400)
        
        # Créer un utilisateur admin temporaire pour created_by si aucun driver
        admin_user = CustomUser.objects.filter(role='admin').first()
        if not admin_user:
            admin_user = CustomUser.objects.create_user(
                username=f'auto_admin_{int(time.time())}',
                email='auto@admin.com',
                password='temp123',
                role='admin'
            )
        
        # Générer un numéro de voyage unique
        import random
        trip_number = f"TRP{random.randint(1000, 9999)}"
        while Trip.objects.filter(trip_number=trip_number).exists():
            trip_number = f"TRP{random.randint(1000, 9999)}"
        
        # Créer le voyage
        trip = Trip.objects.create(
            trip_number=data.get('trip_number') or trip_number,
            departure_city=data['departure_city'],
            arrival_city=data['arrival_city'],
            date=departure_date,
            departure_time=departure_time,
            arrival_time=arrival_time,
            trip_type=data.get('trip_type', 'one_way'),
            status=data.get('status', 'programmed'),
            bus=bus,
            driver=driver,
            price_simple=float(data['price_simple']),
            price_return=float(data['price_return']),
            discount_percent=float(data.get('discount_percent', 0)),
            duration=data.get('duration', ''),
            max_seats=int(data.get('max_seats', bus.total_seats)),
            notes=data.get('notes', ''),
            created_by=driver if driver else admin_user
        )
        
        print(f"DEBUG: Voyage créé avec ID: {trip.id}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Voyage {trip.trip_number} créé avec succès !',
            'trip_id': trip.id,
            'trip_details': {
                'trip_number': trip.trip_number,
                'route': f"{trip.departure_city} → {trip.arrival_city}",
                'date': str(trip.date),
                'time': str(trip.departure_time),
                'price_simple': str(trip.price_simple),
                'price_return': str(trip.price_return),
                'bus': trip.bus.bus_number,
                'driver': f"{trip.driver.first_name} {trip.driver.last_name}" if trip.driver else "Non assigné"
            }
        })
        
    except Exception as e:
        print(f"DEBUG: Erreur lors de la création du voyage: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur: {str(e)}'
        }, status=500)

@csrf_exempt
def list_trips_view(request):
    """API pour lister tous les voyages disponibles - Version simplifiée"""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Méthode GET requise'}, status=405)
    
    try:
        trips = Trip.objects.all()
        trips_data = []
        
        for trip in trips:
            # Version ultra-simplifiée pour éviter les erreurs
            trip_data = {
                'id': trip.id,
                'trip_number': getattr(trip, 'trip_number', f"TRIP-{trip.id}") or f"TRIP-{trip.id}",
                'route': f"{trip.departure_city} → {trip.arrival_city}",
                'departure_city': trip.departure_city,
                'arrival_city': trip.arrival_city,
                'date': str(trip.date),
                'departure_time': str(trip.departure_time),
                'arrival_time': str(getattr(trip, 'arrival_time', '18:00:00') or '18:00:00'),
                'duration': getattr(trip, 'duration', '4h') or '4h',
                'status': getattr(trip, 'status', 'programmed') or 'programmed',
                'price_simple': float(trip.price_simple),
                'price_return': float(trip.price_return),
                'available_seats': trip.max_seats or 25,  # Valeur par défaut
                'max_seats': trip.max_seats or 25,
                'bus_number': getattr(trip.bus, 'bus_number', 'N/A') if hasattr(trip, 'bus') and trip.bus else 'N/A'
            }
            trips_data.append(trip_data)
        
        return JsonResponse({
            'status': 'success',
            'trips': trips_data,
            'total': len(trips_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur: {str(e)}'
        }, status=500)


# Configuration Stripe
import stripe
stripe.api_key = "sk_test_YOUR_STRIPE_SECRET_KEY"  # À remplacer par votre clé secrète

@csrf_exempt
def process_payment_view(request):
    """API pour traiter les paiements Stripe"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode POST requise'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validation des données
        required_fields = ['payment_method_id', 'trip_id', 'trip_type', 'amount']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Le champ {field} est requis'
                }, status=400)
        
        # Vérifier que le voyage existe
        try:
            trip = Trip.objects.get(id=int(data['trip_id']))
        except Trip.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Voyage non trouvé'
            }, status=400)
        
        # Vérifier le montant
        expected_amount = float(trip.price_simple if data['trip_type'] == 'simple' else trip.price_return)
        if float(data['amount']) != expected_amount:
            return JsonResponse({
                'status': 'error',
                'message': 'Montant invalide'
            }, status=400)
        
        # Créer l'intention de paiement Stripe
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(float(data['amount']) * 100),  # Stripe utilise les centimes
                currency='xaf',  # Franc CFA
                payment_method=data['payment_method_id'],
                confirmation_method='manual',
                confirm=True,
                return_url='http://localhost:8009/client-dashboard/',
            )
            
            # Gérer la réponse de Stripe
            if payment_intent.status == 'succeeded':
                # Créer la réservation en base de données avec les bons champs
                booking = Booking.objects.create(
                    trip=trip,
                    client=request.user if request.user.is_authenticated else trip.created_by,
                    passenger_name=f"{request.user.first_name} {request.user.last_name}" if request.user.is_authenticated else "Client Anonyme",
                    passenger_phone=getattr(request.user, 'phone', '+237 000 000 000') if request.user.is_authenticated else "+237 000 000 000",
                    client_email=request.user.email if request.user.is_authenticated else "client@example.com",
                    seats=1,  # Par défaut 1 place
                    trip_type='aller' if data['trip_type'] == 'simple' else 'retour',
                    unit_price=expected_amount,
                    total_price=expected_amount,
                    amount_paid=expected_amount,
                    status='confirmed',
                    payment_method='credit_card',  # Utiliser credit_card au lieu de stripe
                    payment_reference=payment_intent.id
                )
                
                # Note: Les places disponibles sont calculées dynamiquement dans list_trips_view
                
                return JsonResponse({
                    'success': True,
                    'payment_intent': {
                        'id': payment_intent.id,
                        'status': payment_intent.status
                    },
                    'booking': {
                        'id': booking.id,
                        'trip_number': trip.trip_number,
                        'status': booking.status
                    }
                })
            
            elif payment_intent.status == 'requires_action':
                return JsonResponse({
                    'success': False,
                    'requires_action': True,
                    'payment_intent': {
                        'id': payment_intent.id,
                        'client_secret': payment_intent.client_secret
                    }
                })
            
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Paiement échoué'
                })
                
        except stripe.error.CardError as e:
            return JsonResponse({
                'success': False,
                'error': f'Erreur de carte: {e.user_message}'
            })
        except stripe.error.StripeError as e:
            return JsonResponse({
                'success': False,
                'error': f'Erreur de paiement: {str(e)}'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        print(f"DEBUG: Erreur lors du traitement du paiement: {e}")
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)

@csrf_exempt
def list_user_bookings_view(request):
    """API pour lister les réservations d'un utilisateur"""
    if request.method != 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode GET requise'
        }, status=405)
    
    try:
        # Pour l'instant, on prend toutes les réservations (à filtrer par utilisateur plus tard)
        bookings = Booking.objects.all().order_by('-booking_date')
        bookings_data = []
        
        for booking in bookings:
            bookings_data.append({
                'id': booking.id,
                'trip_number': booking.trip.trip_number,
                'route': f"{booking.trip.departure_city} → {booking.trip.arrival_city}",
                'date': str(booking.trip.date),
                'departure_time': str(booking.trip.departure_time),
                'trip_type': booking.trip_type,
                'total_price': str(booking.total_price),
                'status': booking.get_status_display(),
                'booking_date': str(booking.booking_date),
                'payment_method': booking.payment_method,
            })
        
        return JsonResponse({
            'status': 'success',
            'bookings': bookings_data,
            'total': len(bookings_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur: {str(e)}'
        }, status=500)


@csrf_exempt
def create_payment_intent_view(request):
    """API pour créer un Payment Intent Stripe"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode POST requise'
        }, status=405)
    
    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        data = json.loads(request.body)
        
        # Calculs
        unit_price = float(data['unit_price'])
        seat_count = int(data['seat_count'])
        subtotal = unit_price * seat_count
        tax_rate = 18  # 18% TVA
        tax_amount = (subtotal * tax_rate) / 100
        total_amount = subtotal + tax_amount
        
        # Créer le Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),  # Stripe utilise les centimes
            currency='xaf',  # Franc CFA
            metadata={
                'trip_id': data['trip_id'],
                'passenger_name': data['passenger_name'],
                'passenger_email': data['passenger_email'],
                'seat_count': str(seat_count)
            }
        )
        
        return JsonResponse({
            'status': 'success',
            'client_secret': intent.client_secret,
            'amount': total_amount
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': f'Erreur lors de la création du paiement: {str(e)}'
        }, status=500)


@csrf_exempt
def confirm_booking_view(request):
    """API pour confirmer une réservation après paiement Stripe réussi"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode POST requise'
        }, status=405)
    
    try:
        from .models import Trip, Booking, Invoice
        from datetime import datetime, timedelta
        import uuid
        
        data = json.loads(request.body)
        
        # Vérifier le voyage
        trip = Trip.objects.get(id=data['trip_id'])
        
        # Calculs
        unit_price = float(data['unit_price'])
        seat_count = int(data['seat_count'])
        subtotal = unit_price * seat_count
        tax_rate = 18
        tax_amount = (subtotal * tax_rate) / 100
        total_amount = subtotal + tax_amount
        
        # Créer la réservation
        booking = Booking.objects.create(
            booking_reference=f"BK-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}",
            ticket_number=f"TK-{uuid.uuid4().hex[:12].upper()}",
            trip=trip,
            client_id=1,  # À adapter selon l'authentification
            passenger_name=data['passenger_name'],
            passenger_phone=data['passenger_phone'],
            client_email=data['passenger_email'],
            seats=seat_count,
            trip_type=data['trip_type'],
            unit_price=unit_price,
            total_price=total_amount,
            amount_paid=total_amount,
            payment_method='credit_card',
            payment_reference=data['payment_intent_id'],
            status='paid',
            payment_confirmed_at=timezone.now()
        )
        
        # Créer la facture
        invoice = Invoice.objects.create(
            booking=booking,
            client_id=1,  # À adapter selon l'authentification
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total_amount=total_amount,
            stripe_payment_intent_id=data['payment_intent_id'],
            stripe_payment_status='succeeded',
            billing_name=data['cardholder_name'],
            billing_email=data['passenger_email'],
            billing_phone=data['passenger_phone'],
            billing_address=data.get('billing_address', ''),
            status='paid',
            due_date=datetime.now().date() + timedelta(days=30),
            payment_date=timezone.now()
        )
        
        # Générer le PDF de la facture
        pdf_url = generate_invoice_pdf(invoice)
        
        return JsonResponse({
            'status': 'success',
            'booking_id': booking.booking_reference,
            'invoice_number': invoice.invoice_number,
            'invoice_url': f'/api/invoice/download/{invoice.invoice_number}/'
        })
        
    except Trip.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'error': 'Voyage non trouvé'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': f'Erreur lors de la confirmation: {str(e)}'
        }, status=500)


def generate_invoice_pdf(invoice):
    """Générer le PDF de la facture"""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from io import BytesIO
    import os
    
    try:
        # Créer le répertoire s'il n'existe pas
        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices', 'pdf')
        os.makedirs(invoice_dir, exist_ok=True)
        
        # Nom du fichier
        filename = f"facture_{invoice.invoice_number}.pdf"
        filepath = os.path.join(invoice_dir, filename)
        
        # Créer le document PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # En-tête de l'entreprise
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50')
        )
        
        story.append(Paragraph("ROADSHIEL SENTINELLE", title_style))
        story.append(Paragraph("Service de Transport Inter-urbain", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Informations de la facture
        invoice_info = [
            ['Facture N°:', invoice.invoice_number],
            ['Date d\'émission:', invoice.issue_date.strftime('%d/%m/%Y')],
            ['Date d\'échéance:', invoice.due_date.strftime('%d/%m/%Y')],
            ['Statut:', invoice.get_status_display()],
        ]
        
        invoice_table = Table(invoice_info, colWidths=[2*inch, 2*inch])
        invoice_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(invoice_table)
        story.append(Spacer(1, 30))
        
        # Informations du client
        story.append(Paragraph("FACTURÉ À:", styles['Heading3']))
        story.append(Paragraph(f"<b>{invoice.billing_name}</b>", styles['Normal']))
        story.append(Paragraph(invoice.billing_email, styles['Normal']))
        if invoice.billing_phone:
            story.append(Paragraph(invoice.billing_phone, styles['Normal']))
        if invoice.billing_address:
            story.append(Paragraph(invoice.billing_address, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Détails du voyage
        booking = invoice.booking
        trip = booking.trip
        
        story.append(Paragraph("DÉTAILS DU VOYAGE:", styles['Heading3']))
        
        trip_data = [
            ['Référence voyage:', trip.trip_number or f"TRIP-{trip.id}"],
            ['Itinéraire:', f"{trip.departure_city} → {trip.arrival_city}"],
            ['Date de départ:', trip.date.strftime('%d/%m/%Y')],
            ['Heure de départ:', str(trip.departure_time)],
            ['Type de voyage:', booking.get_trip_type_display()],
            ['Nombre de places:', str(booking.seats)],
            ['Passager:', booking.passenger_name],
        ]
        
        trip_table = Table(trip_data, colWidths=[2*inch, 3*inch])
        trip_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(trip_table)
        story.append(Spacer(1, 30))
        
        # Détails financiers
        story.append(Paragraph("DÉTAILS DE FACTURATION:", styles['Heading3']))
        
        financial_data = [
            ['Désignation', 'Quantité', 'Prix unitaire', 'Total'],
            [f'Billet {booking.get_trip_type_display()}', str(booking.seats), f"{booking.unit_price} FCFA", f"{invoice.subtotal} FCFA"],
            ['', '', 'Sous-total:', f"{invoice.subtotal} FCFA"],
            ['', '', f'TVA ({invoice.tax_rate}%):', f"{invoice.tax_amount} FCFA"],
            ['', '', 'TOTAL À PAYER:', f"{invoice.total_amount} FCFA"],
        ]
        
        financial_table = Table(financial_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (-2, -2), (-1, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(financial_table)
        story.append(Spacer(1, 30))
        
        # Informations de paiement
        if invoice.stripe_payment_intent_id:
            story.append(Paragraph("PAIEMENT:", styles['Heading3']))
            story.append(Paragraph(f"Méthode: Carte bancaire (Stripe)", styles['Normal']))
            story.append(Paragraph(f"Référence: {invoice.stripe_payment_intent_id}", styles['Normal']))
            story.append(Paragraph(f"Date de paiement: {invoice.payment_date.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        
        story.append(Spacer(1, 40))
        story.append(Paragraph("Merci pour votre confiance !", styles['Normal']))
        story.append(Paragraph("RoadShiel Sentinelle - Transport sécurisé", styles['Normal']))
        
        # Générer le PDF
        doc.build(story)
        
        # Mettre à jour le modèle avec le chemin du fichier
        invoice.pdf_file = f'invoices/pdf/{filename}'
        invoice.save()
        
        return f'/media/invoices/pdf/{filename}'
        
    except Exception as e:
        print(f"Erreur lors de la génération PDF: {str(e)}")
        return None


@csrf_exempt
def download_invoice_view(request, invoice_number):
    """API pour télécharger une facture PDF"""
    try:
        from .models import Invoice
        from django.http import FileResponse, Http404
        import os
        
        invoice = Invoice.objects.get(invoice_number=invoice_number)
        
        if invoice.pdf_file and os.path.exists(invoice.pdf_file.path):
            response = FileResponse(
                open(invoice.pdf_file.path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="facture_{invoice_number}.pdf"'
            return response
        else:
            # Régénérer le PDF s'il n'existe pas
            pdf_url = generate_invoice_pdf(invoice)
            if pdf_url and os.path.exists(invoice.pdf_file.path):
                response = FileResponse(
                    open(invoice.pdf_file.path, 'rb'),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = f'attachment; filename="facture_{invoice_number}.pdf"'
                return response
            else:
                raise Http404("Facture PDF non disponible")
        
    except Invoice.DoesNotExist:
        raise Http404("Facture non trouvée")
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': f'Erreur: {str(e)}'
        }, status=500)


@csrf_exempt  
def test_trips_view(request):
    """Vue de test ultra-simple"""
    return JsonResponse({
        'status': 'success',
        'message': 'API de test fonctionne',
        'trips': []
    })

@csrf_exempt
@csrf_exempt
def delete_trip_view(request, trip_id):
    """Supprimer un voyage"""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        # Pour le test, on simplifie en enlevant temporairement la vérification d'auth
        # TODO: Remettre la vérification d'authentification
        
        # Supprimer le voyage
        trip = Trip.objects.get(id=trip_id)
        trip_info = f"{trip.departure_city} → {trip.arrival_city} ({trip.date})"
        trip.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Voyage {trip_info} supprimé avec succès'
        })
        
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Voyage non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

@csrf_exempt
def update_trip_view(request, trip_id):
    """Mettre à jour un voyage"""
    if request.method != 'PUT':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        # Pour le test, on simplifie en enlevant temporairement la vérification d'auth
        # TODO: Remettre la vérification d'authentification
        
        # Parser les données JSON
        data = json.loads(request.body)
        
        # Récupérer le voyage
        trip = Trip.objects.get(id=trip_id)
        
        # Mettre à jour les champs
        if 'trip_number' in data:
            trip.trip_number = data['trip_number']
        if 'departure_city' in data:
            trip.departure_city = data['departure_city']
        if 'arrival_city' in data:
            trip.arrival_city = data['arrival_city']
        if 'date' in data:
            trip.date = data['date']
        if 'departure_time' in data:
            trip.departure_time = data['departure_time']
        if 'arrival_time' in data:
            trip.arrival_time = data['arrival_time']
        if 'duration' in data:
            trip.duration = data['duration']
        if 'trip_type' in data:
            trip.trip_type = data['trip_type']
        if 'status' in data:
            trip.status = data['status']
        if 'price_simple' in data:
            trip.price_simple = data['price_simple']
        if 'price_return' in data:
            trip.price_return = data['price_return']
        if 'discount_percent' in data:
            trip.discount_percent = data['discount_percent']
        if 'max_seats' in data:
            trip.max_seats = data['max_seats']
        if 'notes' in data:
            trip.notes = data['notes']
        
        # Gérer le bus si fourni
        if 'bus_id' in data:
            try:
                bus = Bus.objects.get(id=data['bus_id'])
                trip.bus = bus
            except Bus.DoesNotExist:
                return JsonResponse({'error': 'Bus non trouvé'}, status=404)
        
        trip.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Voyage mis à jour avec succès',
            'trip': {
                'id': trip.id,
                'trip_number': trip.trip_number,
                'departure_city': trip.departure_city,
                'arrival_city': trip.arrival_city,
                'date': trip.date,
                'departure_time': trip.departure_time,
                'arrival_time': trip.arrival_time,
                'duration': trip.duration,
                'price_simple': trip.price_simple,
                'price_return': trip.price_return,
                'max_seats': trip.max_seats,
                'available_seats': trip.available_seats,
                'bus': {
                    'id': trip.bus.id if trip.bus else None,
                    'bus_number': trip.bus.bus_number if trip.bus else None
                }
            }
        })
        
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Voyage non trouvé'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

@csrf_exempt
def get_trip_view(request, trip_id):
    """Récupérer les détails d'un voyage"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        trip = Trip.objects.get(id=trip_id)
        
        return JsonResponse({
            'status': 'success',
            'trip': {
                'id': trip.id,
                'trip_number': trip.trip_number,
                'departure_city': trip.departure_city,
                'arrival_city': trip.arrival_city,
                'date': trip.date,
                'departure_time': trip.departure_time,
                'arrival_time': trip.arrival_time,
                'duration': trip.duration,
                'price_simple': trip.price_simple,
                'price_return': trip.price_return,
                'max_seats': trip.max_seats,
                'available_seats': trip.available_seats,
                'bus': {
                    'id': trip.bus.id if trip.bus else None,
                    'bus_number': trip.bus.bus_number if trip.bus else None
                }
            }
        })
        
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Voyage non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

# Vues pour la gestion des chauffeurs
@csrf_exempt
def list_drivers_view(request):
    """API pour lister tous les chauffeurs"""
    try:
        drivers = CustomUser.objects.filter(role='driver').order_by('username')
        drivers_data = []
        
        for driver in drivers:
            drivers_data.append({
                'id': driver.id,
                'username': driver.username,
                'first_name': driver.first_name,
                'last_name': driver.last_name,
                'email': driver.email,
                'phone': driver.phone,
                'license_number': driver.license_number,
                'experience_years': driver.experience_years,
                'rating': driver.rating,
                'is_available': driver.is_available,
                'created_at': driver.created_at.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({
            'status': 'success',
            'drivers': drivers_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur lors du chargement des chauffeurs: {str(e)}'
        })

@csrf_exempt  
def create_driver_view(request):
    """API pour créer un nouveau chauffeur"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        
        # Créer le chauffeur
        driver = CustomUser.objects.create_user(
            username=data.get('username'),
            password=data.get('password', 'password123'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            role='driver',
            license_number=data.get('license_number', ''),
            experience_years=int(data.get('experience_years', 0))
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Chauffeur {driver.username} créé avec succès',
            'driver': {
                'id': driver.id,
                'username': driver.username,
                'first_name': driver.first_name,
                'last_name': driver.last_name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur lors de la création: {str(e)}'
        })

@csrf_exempt
def update_driver_view(request, driver_id):
    """API pour modifier un chauffeur"""
    if request.method != 'PUT':
        return JsonResponse({'status': 'error', 'message': 'PUT required'}, status=405)
    
    try:
        driver = CustomUser.objects.get(id=driver_id, role='driver')
        data = json.loads(request.body.decode('utf-8'))
        
        driver.first_name = data.get('first_name', driver.first_name)
        driver.last_name = data.get('last_name', driver.last_name)
        driver.email = data.get('email', driver.email)
        driver.phone = data.get('phone', driver.phone)
        driver.license_number = data.get('license_number', driver.license_number)
        driver.experience_years = int(data.get('experience_years', driver.experience_years))
        driver.is_available = data.get('is_available', driver.is_available)
        
        driver.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Chauffeur {driver.username} modifié avec succès'
        })
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Chauffeur non trouvé'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Erreur: {str(e)}'})

@csrf_exempt
def delete_driver_view(request, driver_id):
    """API pour supprimer un chauffeur"""
    if request.method != 'DELETE':
        return JsonResponse({'status': 'error', 'message': 'DELETE required'}, status=405)
    
    try:
        driver = CustomUser.objects.get(id=driver_id, role='driver')
        driver_name = f"{driver.first_name} {driver.last_name}"
        driver.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Chauffeur {driver_name} supprimé avec succès'
        })
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Chauffeur non trouvé'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Erreur: {str(e)}'})

@csrf_exempt
def rate_driver_view(request, driver_id):
    """API pour noter un chauffeur"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)
    
    try:
        driver = CustomUser.objects.get(id=driver_id, role='driver')
        data = json.loads(request.body.decode('utf-8'))
        
        new_rating = float(data.get('new_rating', 0))
        if new_rating < 1 or new_rating > 5:
            return JsonResponse({
                'status': 'error', 
                'message': 'La note doit être entre 1 et 5'
            })
        
        # Ajouter la nouvelle note
        driver.add_rating(new_rating)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Note {new_rating}/5 ajoutée. Nouvelle moyenne: {driver.rating:.1f}/5',
            'new_average': round(driver.rating, 1),
            'total_ratings': driver.total_ratings
        })
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Chauffeur non trouvé'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Erreur: {str(e)}'})

@csrf_protect
def login_client(request):
    """Vue Django traditionnelle pour la connexion client sans JavaScript"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Nom d\'utilisateur et mot de passe requis')
            return redirect('/login/')
        
        # Authentification
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Vérifier que c'est un client (pas un admin)
            if user.is_staff:
                messages.error(request, 'Ce compte n\'est pas un compte client')
                return redirect('/login/')
            
            # Connexion réussie
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            
            # Redirection vers le dashboard client
            return redirect('/client-dashboard/')
        else:
            # Authentification échouée
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            return redirect('/login/')
    
    # Si GET ou autre méthode, rediriger vers login
    return redirect('/login/')