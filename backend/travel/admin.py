from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Bus, Trip, Booking, SomnolenceAlert
from .models import DriverProfile, Report

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'rating', 'is_available')
    list_filter = ('role', 'is_staff', 'is_active', 'is_available', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'license_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone', 'date_of_birth', 'address')
        }),
        ('Informations chauffeur', {
            'fields': ('rating', 'license_number', 'experience_years', 'is_available', 'total_ratings'),
            'classes': ('collapse',)
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone', 'date_of_birth', 'address')
        }),
    )

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'bus_model', 'total_seats', 'status', 'assigned_driver', 'year', 'mileage')
    list_filter = ('status', 'year', 'assigned_driver')
    search_fields = ('bus_number', 'bus_model', 'assigned_driver__username')
    readonly_fields = ('created_at',)
    ordering = ('bus_number',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('bus_number', 'bus_model', 'total_seats', 'year', 'status')
        }),
        ('Assignation', {
            'fields': ('assigned_driver',)
        }),
        ('Technique', {
            'fields': ('mileage', 'arduino_device_id'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_number', 'departure_city', 'arrival_city', 'date', 'departure_time', 'bus', 'driver', 'status', 'get_available_seats')
    list_filter = ('status', 'trip_type', 'date', 'bus', 'driver')
    search_fields = ('trip_number', 'departure_city', 'arrival_city', 'bus__bus_number')
    readonly_fields = ('trip_number', 'created_at', 'get_available_seats', 'get_occupancy_rate')
    date_hierarchy = 'date'
    ordering = ('-date', 'departure_time')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('trip_number', 'departure_city', 'arrival_city', 'trip_type', 'status')
        }),
        ('Horaires', {
            'fields': ('date', 'departure_time', 'arrival_date', 'arrival_time', 'duration')
        }),
        ('Ressources', {
            'fields': ('bus', 'driver', 'max_seats')
        }),
        ('Tarification', {
            'fields': ('price_simple', 'price_return', 'discount_percent')
        }),
        ('Statistiques', {
            'fields': ('get_available_seats', 'get_occupancy_rate'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_available_seats(self, obj):
        return obj.available_seats
    get_available_seats.short_description = 'Places disponibles'
    
    def get_occupancy_rate(self, obj):
        return f"{obj.occupancy_rate:.1f}%"
    get_occupancy_rate.short_description = 'Taux occupation'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'ticket_number', 'passenger_name', 'trip', 'seats', 'status', 'total_price', 'get_payment_status', 'booking_date')
    list_filter = ('status', 'trip_type', 'payment_method', 'booking_date')
    search_fields = ('booking_reference', 'ticket_number', 'passenger_name', 'client_email', 'passenger_phone')
    readonly_fields = ('booking_reference', 'ticket_number', 'booking_date', 'get_payment_progress', 'get_remaining_amount')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    
    fieldsets = (
        ('Informations réservation', {
            'fields': ('booking_reference', 'ticket_number', 'trip', 'status')
        }),
        ('Passager', {
            'fields': ('client', 'passenger_name', 'passenger_phone', 'client_email')
        }),
        ('Voyage', {
            'fields': ('seats', 'seat_numbers', 'trip_type')
        }),
        ('Paiement', {
            'fields': ('unit_price', 'discount_applied', 'total_price', 'amount_paid', 'payment_method', 'payment_reference', 'payment_phone', 'payment_confirmed_at')
        }),
        ('Statut', {
            'fields': ('get_payment_progress', 'get_remaining_amount'),
            'classes': ('collapse',)
        }),
        ('Validation/Annulation', {
            'fields': ('validated_at', 'validated_by', 'cancelled_at', 'cancelled_by', 'cancellation_reason'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes', 'special_requests'),
            'classes': ('collapse',)
        }),
    )
    
    def get_payment_status(self, obj):
        if obj.is_fully_paid:
            return "✅ Payé"
        elif obj.amount_paid > 0:
            return f"⚠️ Partiel ({obj.payment_progress:.1f}%)"
        else:
            return "❌ Non payé"
    get_payment_status.short_description = 'Paiement'
    
    def get_payment_progress(self, obj):
        return f"{obj.payment_progress:.1f}%"
    get_payment_progress.short_description = 'Progression paiement'
    
    def get_remaining_amount(self, obj):
        return f"{obj.remaining_amount} €"
    get_remaining_amount.short_description = 'Montant restant'

@admin.register(SomnolenceAlert)
class SomnolenceAlertAdmin(admin.ModelAdmin):
    list_display = ('alert_id', 'bus', 'driver', 'duration_seconds', 'severity', 'status', 'timestamp', 'handled', 'get_age')
    list_filter = ('handled', 'severity', 'status', 'escalated', 'timestamp')
    readonly_fields = ('alert_id', 'raw_data', 'timestamp', 'get_age', 'get_response_time')
    search_fields = ('alert_id', 'bus__bus_number', 'driver__username')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Informations alerte', {
            'fields': ('alert_id', 'timestamp', 'get_age', 'severity', 'status')
        }),
        ('Contexte', {
            'fields': ('bus', 'driver', 'trip', 'duration_seconds')
        }),
        ('Localisation', {
            'fields': ('location_latitude', 'location_longitude'),
            'classes': ('collapse',)
        }),
        ('Données techniques', {
            'fields': ('arduino_device_id', 'sensor_confidence', 'raw_data'),
            'classes': ('collapse',)
        }),
        ('Traitement', {
            'fields': ('handled', 'handled_at', 'handled_by', 'action_taken', 'get_response_time')
        }),
        ('Escalade', {
            'fields': ('escalated', 'escalated_to', 'follow_up_required'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_age(self, obj):
        return f"{obj.age_minutes:.0f} min"
    get_age.short_description = 'Âge'
    
    def get_response_time(self, obj):
        if obj.response_time:
            return f"{obj.response_time.total_seconds():.0f} sec"
        return "Non traitée"
    get_response_time.short_description = 'Temps réponse'

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'rating', 'license_number', 'is_available')
    list_filter = ('is_available', 'experience_years', 'rating')
    search_fields = ('username', 'first_name', 'last_name', 'license_number', 'email')
    ordering = ('-rating', 'last_name', 'first_name')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('title', 'content', 'created_by__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
