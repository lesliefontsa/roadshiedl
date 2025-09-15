# travel/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from datetime import datetime

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('client', 'Client'),
        ('driver', 'Chauffeur'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Champs pour chauffeurs
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    total_ratings = models.PositiveIntegerField(default=0)
    license_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    # Adresse complète pour tous les utilisateurs
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def average_rating(self):
        return self.rating if self.total_ratings > 0 else 0.0
    
    def add_rating(self, new_rating):
        """Ajouter une nouvelle note au chauffeur"""
        if 0 <= new_rating <= 5:
            total_score = self.rating * self.total_ratings
            self.total_ratings += 1
            self.rating = (total_score + new_rating) / self.total_ratings
            self.save()

class Bus(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_route', 'En Route'),
        ('maintenance', 'En Maintenance'),
        ('hors_service', 'Hors Service'),
        ('en_panne', 'En Panne'),
    ]
    
    bus_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro du bus")
    bus_model = models.CharField(max_length=100, verbose_name="Modèle")
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Nombre de places")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Année")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible', verbose_name="Statut")
    mileage = models.PositiveIntegerField(default=0, verbose_name="Kilométrage")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Assignation du chauffeur
    assigned_driver = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_buses',
        limit_choices_to={'role': 'driver'},
        verbose_name="Chauffeur assigné"
    )
    
    # ID Arduino pour IoT
    arduino_device_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.bus_number} - {self.bus_model}"
    
    @property
    def is_available_for_assignment(self):
        """Vérifie si le bus peut être assigné pour un voyage"""
        return self.status == 'disponible' and self.assigned_driver is not None

class Trip(models.Model):
    TRIP_TYPE_CHOICES = [
        ('one_way', 'Aller simple'),
        ('round_trip', 'Aller-retour'),
        ('recurring', 'Régulier'),
    ]
    
    STATUS_CHOICES = [
        ('programmed', 'Programmé'),
        ('boarding', 'Embarquement'),
        ('in_transit', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
        ('delayed', 'Retardé'),
    ]
    
    trip_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de voyage", default="TMP-TRIP")
    departure_city = models.CharField(max_length=100, verbose_name="Ville de départ")
    arrival_city = models.CharField(max_length=100, verbose_name="Ville d'arrivée")
    date = models.DateField(verbose_name="Date de départ")
    departure_time = models.TimeField(verbose_name="Heure de départ")
    arrival_date = models.DateField(blank=True, null=True, verbose_name="Date d'arrivée")
    arrival_time = models.TimeField(blank=True, null=True, verbose_name="Heure d'arrivée")
    duration = models.CharField(max_length=20, blank=True, null=True, verbose_name="Durée estimée")
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES, default='one_way', verbose_name="Type de voyage")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='programmed', verbose_name="Statut")
    
    # Relations
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Bus assigné")
    driver = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'driver'},
        related_name='trips_as_driver',
        verbose_name="Chauffeur"
    )
    
    # Tarifs
    price_simple = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix aller simple")
    price_return = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix aller-retour")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Réduction (%)")
    
    # Gestion
    max_seats = models.PositiveIntegerField(blank=True, null=True, verbose_name="Places maximum")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_trips', verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Auto-assigner le chauffeur du bus si non spécifié
        if not self.driver and self.bus.assigned_driver:
            self.driver = self.bus.assigned_driver
        
        # Auto-définir le nombre max de places si non spécifié
        if not self.max_seats:
            self.max_seats = self.bus.total_seats
            
        # Générer un numéro de voyage si non fourni
        if not self.trip_number:
            self.trip_number = self.generate_trip_number()
        
        # Auto-calculer date/heure d'arrivée si non fournie
        if not self.arrival_date:
            self.arrival_date = self.date
        
        super().save(*args, **kwargs)
    
    def generate_trip_number(self):
        """Génère un numéro de voyage unique"""
        date_str = self.date.strftime("%Y%m%d")
        origin_code = self.departure_city[:3].upper()
        dest_code = self.arrival_city[:3].upper()
        
        # Compter les voyages existants pour cette date avec incrément
        existing_count = Trip.objects.filter(date=self.date).count()
        attempt = 0
        max_attempts = 100
        
        while attempt < max_attempts:
            count = existing_count + attempt + 1
            trip_number = f"{date_str}-{origin_code}{dest_code}-{count:03d}"
            
            # Vérifier si ce numéro existe déjà
            if not Trip.objects.filter(trip_number=trip_number).exists():
                return trip_number
            
            attempt += 1
        
        # En dernier recours, utiliser un timestamp
        import time
        timestamp = str(int(time.time()))[-6:]
        return f"{date_str}-{origin_code}{dest_code}-{timestamp}"
    
    @property
    def available_seats(self):
        """Retourne le nombre de places disponibles"""
        booked_seats = self.bookings.filter(
            status__in=['confirmed', 'validated']
        ).aggregate(total=models.Sum('seats'))['total'] or 0
        max_seats = self.max_seats or self.bus.total_seats
        return max_seats - booked_seats
    
    @property
    def is_fully_booked(self):
        """Vérifie si le voyage est complet"""
        return self.available_seats <= 0
    
    @property
    def occupancy_rate(self):
        """Taux d'occupation en pourcentage"""
        max_seats = self.max_seats or self.bus.total_seats
        if max_seats == 0:
            return 0
        booked_seats = max_seats - self.available_seats
        return (booked_seats / max_seats) * 100
    
    @property
    def effective_price_simple(self):
        """Prix effectif aller simple après réduction"""
        if self.discount_percent > 0:
            return self.price_simple * (1 - self.discount_percent / 100)
        return self.price_simple
    
    @property
    def effective_price_return(self):
        """Prix effectif aller-retour après réduction"""
        if self.discount_percent > 0:
            return self.price_return * (1 - self.discount_percent / 100)
        return self.price_return
    
    def can_be_cancelled(self):
        """Vérifie si le voyage peut être annulé"""
        now = timezone.now()
        departure_datetime = timezone.datetime.combine(self.date, self.departure_time)
        return departure_datetime > now and self.status in ['programmed', 'delayed']
    
    def __str__(self):
        display_number = self.trip_number or f"Trip-{self.id}"
        return f"{display_number}: {self.departure_city} → {self.arrival_city} - {self.date}"
    
    class Meta:
        ordering = ['date', 'departure_time']
        verbose_name = "Voyage"
        verbose_name_plural = "Voyages"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('partially_paid', 'Partiellement payée'),
        ('paid', 'Payée'),
        ('validated', 'Validée'),
        ('cancelled', 'Annulée'),
        ('refunded', 'Remboursée'),
        ('no_show', 'Absent'),
    ]
    
    TRIP_TYPE_CHOICES = [
        ('aller', 'Aller Simple'),
        ('retour', 'Aller-Retour'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('orange_money', 'Orange Money'),
        ('wave', 'Wave'),
        ('cash', 'Espèces'),
        ('bank_transfer', 'Virement bancaire'),
        ('credit_card', 'Carte bancaire'),
    ]
    
    # Informations de base
    booking_reference = models.CharField(max_length=20, unique=True, verbose_name="Référence de réservation", default="TMP-REF")
    ticket_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de ticket")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings', verbose_name="Voyage")
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Client")
    
    # Détails de la réservation
    passenger_name = models.CharField(max_length=200, verbose_name="Nom du passager", default="Passager")
    passenger_phone = models.CharField(max_length=20, verbose_name="Téléphone du passager", default="N/A")
    client_email = models.EmailField(verbose_name="Email de contact")
    seats = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Nombre de places")
    seat_numbers = models.CharField(max_length=100, blank=True, verbose_name="Numéros de siège")
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE_CHOICES, verbose_name="Type de voyage")
    
    # Informations financières
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire", default=0)
    discount_applied = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Réduction appliquée (%)")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant payé")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, verbose_name="Mode de paiement")
    
    # Informations de paiement mobile/en ligne
    payment_reference = models.CharField(max_length=100, blank=True, null=True, verbose_name="Référence de paiement")
    payment_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone de paiement")
    payment_confirmed_at = models.DateTimeField(blank=True, null=True, verbose_name="Confirmé le")
    
    # Statut et horodatage
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de réservation")
    
    # Validation et annulation
    validated_at = models.DateTimeField(blank=True, null=True, verbose_name="Validé le")
    validated_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='validated_bookings', verbose_name="Validé par"
    )
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name="Annulé le")
    cancelled_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cancelled_bookings', verbose_name="Annulé par"
    )
    cancellation_reason = models.TextField(blank=True, verbose_name="Raison d'annulation")
    
    # Notes et commentaires
    notes = models.TextField(blank=True, verbose_name="Notes")
    special_requests = models.TextField(blank=True, verbose_name="Demandes spéciales")
    
    def save(self, *args, **kwargs):
        # Générer référence de réservation si non fournie
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        
        # Générer numéro de ticket si non fourni
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        
        # Calculer le prix total
        if not self.total_price:
            self.calculate_total_price()
        
        super().save(*args, **kwargs)
    
    def generate_booking_reference(self):
        """Génère une référence de réservation unique"""
        date_str = timezone.now().strftime("%Y%m%d")
        random_str = str(uuid.uuid4())[:8].upper()
        return f"BK{date_str}{random_str}"
    
    def generate_ticket_number(self):
        """Génère un numéro de ticket unique"""
        trip_code = f"{self.trip.departure_city[:2].upper()}{self.trip.arrival_city[:2].upper()}"
        date_str = self.trip.date.strftime("%m%d")
        random_str = str(uuid.uuid4())[:6].upper()
        return f"TK{trip_code}{date_str}{random_str}"
    
    def calculate_total_price(self):
        """Calcule le prix total en fonction du type de voyage et de la réduction"""
        if self.trip_type == 'aller':
            base_price = self.trip.effective_price_simple
        else:
            base_price = self.trip.effective_price_return
        
        self.unit_price = base_price
        subtotal = base_price * self.seats
        
        if self.discount_applied > 0:
            subtotal = subtotal * (1 - self.discount_applied / 100)
        
        self.total_price = subtotal
    
    @property
    def remaining_amount(self):
        """Montant restant à payer"""
        return self.total_price - self.amount_paid
    
    @property
    def is_fully_paid(self):
        """Vérifie si la réservation est entièrement payée"""
        return self.amount_paid >= self.total_price
    
    @property
    def payment_progress(self):
        """Pourcentage de paiement effectué"""
        if self.total_price == 0:
            return 100
        return (self.amount_paid / self.total_price) * 100
    
    def can_be_cancelled(self):
        """Vérifie si la réservation peut être annulée"""
        if self.status in ['cancelled', 'refunded', 'validated']:
            return False
        
        # Vérifier si le voyage n'a pas encore commencé
        return self.trip.can_be_cancelled()
    
    def mark_as_paid(self, payment_method, payment_reference=None):
        """Marque la réservation comme payée"""
        self.status = 'paid'
        self.payment_method = payment_method
        self.payment_reference = payment_reference
        self.payment_confirmed_at = timezone.now()
        self.amount_paid = self.total_price
        self.save()
    
    def partial_payment(self, amount, payment_method, payment_reference=None):
        """Enregistre un paiement partiel"""
        self.amount_paid += amount
        self.payment_method = payment_method
        self.payment_reference = payment_reference
        
        if self.is_fully_paid:
            self.status = 'paid'
            self.payment_confirmed_at = timezone.now()
        else:
            self.status = 'partially_paid'
        
        self.save()
    
    def cancel_booking(self, cancelled_by, reason=""):
        """Annule la réservation"""
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.cancelled_by = cancelled_by
        self.cancellation_reason = reason
        self.save()
    
    def validate_booking(self, validated_by):
        """Valide la réservation (embarquement effectué)"""
        self.status = 'validated'
        self.validated_at = timezone.now()
        self.validated_by = validated_by
        self.save()
    
    def __str__(self):
        return f"{self.booking_reference} - {self.passenger_name} ({self.seats} places)"
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"

class CustomProfile(CustomUser):
    class Meta:
        proxy = True
        app_label = 'travel'
        # model_name will be 'customprofile' (derived from class name)


class SomnolenceAlert(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('critical', 'Critique'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Nouvelle'),
        ('acknowledged', 'Accusée'),
        ('investigating', 'En cours de traitement'),
        ('resolved', 'Résolue'),
        ('false_positive', 'Fausse alerte'),
    ]
    
    # Informations de base
    alert_id = models.CharField(max_length=50, unique=True, verbose_name="ID d'alerte", default="TMP-ALERT")
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bus")
    driver = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'driver'},
        verbose_name="Chauffeur"
    )
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Voyage")
    
    # Détails de l'alerte
    duration_seconds = models.FloatField(verbose_name="Durée (secondes)")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium', verbose_name="Sévérité")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Horodatage")
    location_latitude = models.FloatField(blank=True, null=True, verbose_name="Latitude")
    location_longitude = models.FloatField(blank=True, null=True, verbose_name="Longitude")
    
    # Données techniques
    raw_data = models.JSONField(blank=True, null=True, verbose_name="Données brutes")
    arduino_device_id = models.CharField(max_length=50, blank=True, verbose_name="ID du dispositif Arduino")
    sensor_confidence = models.FloatField(default=0.0, verbose_name="Confiance du capteur")
    
    # Gestion de l'alerte
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Statut")
    handled = models.BooleanField(default=False, verbose_name="Traitée")
    handled_at = models.DateTimeField(blank=True, null=True, verbose_name="Traitée le")
    handled_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='handled_alerts',
        verbose_name="Traitée par"
    )
    
    # Actions prises
    action_taken = models.TextField(blank=True, verbose_name="Action prise")
    follow_up_required = models.BooleanField(default=False, verbose_name="Suivi requis")
    escalated = models.BooleanField(default=False, verbose_name="Escaladée")
    escalated_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalated_alerts',
        verbose_name="Escaladée vers"
    )
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    def save(self, *args, **kwargs):
        # Générer un ID d'alerte si non fourni
        if not self.alert_id:
            self.alert_id = self.generate_alert_id()
        
        # Déterminer la sévérité automatiquement
        if not self.severity or self.severity == 'medium':
            self.severity = self.calculate_severity()
        
        # Associer le voyage actuel du chauffeur si possible
        if not self.trip and self.driver and self.bus:
            current_trip = self.find_current_trip()
            if current_trip:
                self.trip = current_trip
        
        super().save(*args, **kwargs)
    
    def generate_alert_id(self):
        """Génère un ID unique pour l'alerte"""
        timestamp_str = timezone.now().strftime("%Y%m%d%H%M%S")
        random_str = str(uuid.uuid4())[:6].upper()
        return f"ALT{timestamp_str}{random_str}"
    
    def calculate_severity(self):
        """Calcule la sévérité basée sur la durée"""
        if self.duration_seconds >= 5.0:
            return 'critical'
        elif self.duration_seconds >= 3.0:
            return 'high'
        elif self.duration_seconds >= 2.0:
            return 'medium'
        else:
            return 'low'
    
    def find_current_trip(self):
        """Trouve le voyage en cours pour le chauffeur et le bus"""
        now = timezone.now()
        today = now.date()
        current_time = now.time()
        
        # Chercher un voyage en cours
        current_trips = Trip.objects.filter(
            driver=self.driver,
            bus=self.bus,
            date=today,
            departure_time__lte=current_time,
            status__in=['boarding', 'in_transit']
        ).first()
        
        return current_trips
    
    def mark_as_handled(self, handled_by, action_taken="", notes=""):
        """Marque l'alerte comme traitée"""
        self.handled = True
        self.status = 'resolved'
        self.handled_at = timezone.now()
        self.handled_by = handled_by
        if action_taken:
            self.action_taken = action_taken
        if notes:
            self.notes = notes
        self.save()
    
    def escalate_alert(self, escalated_to, reason=""):
        """Escalade l'alerte vers un superviseur"""
        self.escalated = True
        self.escalated_to = escalated_to
        self.status = 'investigating'
        self.follow_up_required = True
        if reason:
            self.notes += f"\nEscaladée: {reason}"
        self.save()
    
    def acknowledge(self, acknowledged_by):
        """Accuse réception de l'alerte"""
        self.status = 'acknowledged'
        self.handled_by = acknowledged_by
        self.save()
    
    @property
    def is_critical(self):
        """Vérifie si l'alerte est critique"""
        return self.severity == 'critical' or self.duration_seconds >= 5.0
    
    @property
    def response_time(self):
        """Temps de réponse à l'alerte"""
        if self.handled_at:
            return self.handled_at - self.timestamp
        return None
    
    @property
    def age_minutes(self):
        """Âge de l'alerte en minutes"""
        return (timezone.now() - self.timestamp).total_seconds() / 60
    
    def __str__(self):
        driver_name = self.driver.get_full_name() if self.driver else "Inconnu"
        bus_info = f"Bus {self.bus.bus_number}" if self.bus else "Bus inconnu"
        return f"{self.alert_id}: {bus_info} - {driver_name} ({self.duration_seconds}s) [{self.severity}]"
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Alerte de somnolence"
        verbose_name_plural = "Alertes de somnolence"


class DriverProfile(CustomUser):
    class Meta:
        proxy = True
        app_label = 'travel'


class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.created_at.date()}"


class Invoice(models.Model):
    """Modèle pour les factures PDF"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ]
    
    # Informations de base
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de facture")
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice', verbose_name="Réservation")
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Client")
    
    # Détails financiers
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sous-total")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Taux de taxe (%)")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant de taxe")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    
    # Paiement Stripe
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID Stripe Payment Intent")
    stripe_payment_status = models.CharField(max_length=50, blank=True, null=True, verbose_name="Statut paiement Stripe")
    
    # Informations de facturation
    billing_name = models.CharField(max_length=200, verbose_name="Nom de facturation")
    billing_email = models.EmailField(verbose_name="Email de facturation")
    billing_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone de facturation")
    billing_address = models.TextField(blank=True, verbose_name="Adresse de facturation")
    
    # Statut et horodatage
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'émission")
    due_date = models.DateField(verbose_name="Date d'échéance")
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="Date de paiement")
    
    # Fichier PDF
    pdf_file = models.FileField(upload_to='invoices/pdf/', blank=True, null=True, verbose_name="Fichier PDF")
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        
        # Calculs automatiques
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount
        
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        """Génère un numéro de facture unique"""
        from datetime import datetime
        prefix = "INV"
        date_part = datetime.now().strftime("%Y%m%d")
        
        # Trouver le dernier numéro de facture du jour
        today_invoices = Invoice.objects.filter(
            invoice_number__startswith=f"{prefix}-{date_part}"
        ).count()
        
        sequence = str(today_invoices + 1).zfill(3)
        return f"{prefix}-{date_part}-{sequence}"
    
    def __str__(self):
        return f"Facture {self.invoice_number} - {self.client.username}"
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name = "Facture"
        verbose_name_plural = "Factures"