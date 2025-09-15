// Client Dashboard JavaScript
class ClientDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8009';
        this.token = localStorage.getItem('authToken');
        this.user = JSON.parse(localStorage.getItem('userInfo') || 'null');
        this.currentTrips = [];
        this.currentBookings = [];
        this.init();
    }

    async init() {
        // Vérifier l'authentification
        if (!this.token || !this.user) {
            this.redirectToLogin();
            return;
        }

        // Vérifier que c'est un client
        if (this.user.role !== 'client') {
            this.redirectToLogin();
            return;
        }

        // Afficher les informations client
        this.displayClientInfo();

        // Charger les données
        await this.loadAvailableTrips();
        await this.loadMyBookings();

        // Configurer les événements
        this.setupEventListeners();

        // Définir la date par défaut à aujourd'hui
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('travelDate').value = today;
    }

    redirectToLogin() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        window.location.href = '/auth/login/';
    }

    displayClientInfo() {
        const userName = document.getElementById('userName');
        if (userName && this.user) {
            userName.textContent = `${this.user.first_name} ${this.user.last_name}`;
        }
    }

    setupEventListeners() {
        // Formulaire de recherche
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchTrips();
        });

        // Formulaire de réservation
        document.getElementById('bookingForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.confirmBooking();
        });

        // Mise à jour du total lors du changement du nombre de places
        document.getElementById('seatCount').addEventListener('change', () => {
            this.updateTotalAmount();
        });

        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                if (link.getAttribute('href').startsWith('#')) {
                    e.preventDefault();
                    const target = link.getAttribute('href').substring(1);
                    this.showSection(target);
                }
            });
        });
    }

    showSection(sectionName) {
        // Marquer le lien actif
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + sectionName) {
                link.classList.add('active');
            }
        });

        // Faire défiler vers la section
        const section = document.getElementById(sectionName);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }

    async loadAvailableTrips() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/trips/list/`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.currentTrips = data.trips || [];
                this.displayTrips(this.currentTrips);
            } else {
                this.showError('Erreur lors du chargement des voyages');
            }
        } catch (error) {
            console.error('Erreur chargement voyages:', error);
            this.showError('Erreur de connexion au serveur');
        }
    }

    displayTrips(trips) {
        const container = document.getElementById('tripsContainer');
        
        if (trips.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">Aucun voyage disponible</h4>
                    <p class="text-muted">Essayez de modifier vos critères de recherche</p>
                </div>
            `;
            return;
        }

        const html = trips.map(trip => `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card trip-card h-100">
                    <div class="card-header bg-primary text-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">${trip.departure_city} → ${trip.arrival_city}</h6>
                            <span class="price-badge">${new Intl.NumberFormat('fr-FR').format(trip.price)} XAF</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <div class="row">
                                <div class="col-6">
                                    <small class="text-muted">Départ</small><br>
                                    <strong>${new Date(trip.departure_time).toLocaleDateString('fr-FR')}</strong><br>
                                    <small>${new Date(trip.departure_time).toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'})}</small>
                                </div>
                                <div class="col-6">
                                    <small class="text-muted">Arrivée</small><br>
                                    <strong>${new Date(trip.arrival_time).toLocaleDateString('fr-FR')}</strong><br>
                                    <small>${new Date(trip.arrival_time).toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'})}</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="d-flex justify-content-between align-items-center">
                                <span><i class="fas fa-bus"></i> ${trip.bus?.registration_number || 'N/A'}</span>
                                <span class="badge bg-info">${trip.available_seats} places</span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <small class="text-muted">Équipements :</small><br>
                            ${trip.bus?.has_ac ? '<i class="fas fa-snowflake text-info" title="Climatisation"></i> ' : ''}
                            ${trip.bus?.has_wifi ? '<i class="fas fa-wifi text-success" title="WiFi"></i> ' : ''}
                            ${!trip.bus?.has_ac && !trip.bus?.has_wifi ? '<span class="text-muted">Standard</span>' : ''}
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-primary w-100" onclick="showBookingModal('${trip.id}')" ${trip.available_seats === 0 ? 'disabled' : ''}>
                            <i class="fas fa-ticket-alt"></i> 
                            ${trip.available_seats === 0 ? 'Complet' : 'Réserver'}
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    async loadMyBookings() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/bookings/my/`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.currentBookings = data.bookings || [];
                this.displayBookings(this.currentBookings);
            } else {
                this.showError('Erreur lors du chargement de vos réservations');
            }
        } catch (error) {
            console.error('Erreur chargement réservations:', error);
            this.showError('Erreur de connexion au serveur');
        }
    }

    displayBookings(bookings) {
        const container = document.getElementById('bookingsContainer');
        
        if (bookings.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-3">
                    <i class="fas fa-ticket-alt fa-2x text-muted mb-3"></i>
                    <h5 class="text-muted">Aucune réservation</h5>
                    <p class="text-muted">Vous n'avez pas encore effectué de réservation</p>
                </div>
            `;
            return;
        }

        const html = bookings.map(booking => `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card booking-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <h6 class="card-title">${booking.trip?.departure_city} → ${booking.trip?.arrival_city}</h6>
                            <span class="badge status-badge bg-${this.getStatusColor(booking.status)}">${this.getStatusText(booking.status)}</span>
                        </div>
                        
                        <div class="mb-2">
                            <strong>N° de réservation :</strong> <code>${booking.booking_number}</code>
                        </div>
                        
                        <div class="mb-2">
                            <strong>Date :</strong> ${new Date(booking.trip?.departure_time).toLocaleDateString('fr-FR')}
                        </div>
                        
                        <div class="mb-2">
                            <strong>Heure :</strong> ${new Date(booking.trip?.departure_time).toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'})}
                        </div>
                        
                        <div class="mb-2">
                            <strong>Places :</strong> ${booking.seat_count}
                        </div>
                        
                        <div class="mb-3">
                            <strong>Total :</strong> ${new Intl.NumberFormat('fr-FR').format(booking.total_amount)} XAF
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button class="btn btn-outline-primary btn-sm" onclick="viewBookingDetails('${booking.booking_number}')">
                                <i class="fas fa-eye"></i> Détails
                            </button>
                            ${booking.status === 'confirmed' ? `
                                <button class="btn btn-outline-success btn-sm" onclick="downloadTicket('${booking.booking_number}')">
                                    <i class="fas fa-download"></i> Ticket
                                </button>
                            ` : ''}
                            ${booking.status === 'pending' ? `
                                <button class="btn btn-outline-danger btn-sm" onclick="cancelBooking('${booking.booking_number}')">
                                    <i class="fas fa-times"></i> Annuler
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    getStatusColor(status) {
        switch(status) {
            case 'confirmed': return 'success';
            case 'pending': return 'warning';
            case 'cancelled': return 'danger';
            default: return 'secondary';
        }
    }

    getStatusText(status) {
        switch(status) {
            case 'confirmed': return 'Confirmé';
            case 'pending': return 'En attente';
            case 'cancelled': return 'Annulé';
            default: return status;
        }
    }

    searchTrips() {
        const departure = document.getElementById('departure').value.toLowerCase();
        const destination = document.getElementById('destination').value.toLowerCase();
        const travelDate = document.getElementById('travelDate').value;

        let filteredTrips = this.currentTrips;

        if (departure) {
            filteredTrips = filteredTrips.filter(trip => 
                trip.departure_city.toLowerCase().includes(departure)
            );
        }

        if (destination) {
            filteredTrips = filteredTrips.filter(trip => 
                trip.arrival_city.toLowerCase().includes(destination)
            );
        }

        if (travelDate) {
            filteredTrips = filteredTrips.filter(trip => {
                const tripDate = new Date(trip.departure_time).toISOString().split('T')[0];
                return tripDate === travelDate;
            });
        }

        this.displayTrips(filteredTrips);

        // Faire défiler vers les résultats
        document.getElementById('tripsContainer').scrollIntoView({ behavior: 'smooth' });
    }

    showBookingModal(tripId) {
        const trip = this.currentTrips.find(t => t.id == tripId);
        if (!trip) return;

        // Remplir les détails du voyage
        document.getElementById('tripDetails').innerHTML = `
            <div class="alert alert-info">
                <h6><i class="fas fa-route"></i> ${trip.departure_city} → ${trip.arrival_city}</h6>
                <p class="mb-1"><strong>Départ :</strong> ${new Date(trip.departure_time).toLocaleString('fr-FR')}</p>
                <p class="mb-1"><strong>Bus :</strong> ${trip.bus?.registration_number} (${trip.bus?.brand} ${trip.bus?.model})</p>
                <p class="mb-0"><strong>Prix par place :</strong> ${new Intl.NumberFormat('fr-FR').format(trip.price)} XAF</p>
            </div>
        `;

        // Remplir l'ID du voyage
        document.getElementById('selectedTripId').value = tripId;

        // Remplir les informations client si disponibles
        if (this.user) {
            document.getElementById('passengerName').value = `${this.user.first_name} ${this.user.last_name}`;
            document.getElementById('passengerEmail').value = this.user.email || '';
        }

        // Calculer le montant initial
        this.updateTotalAmount();

        // Afficher la modal
        new bootstrap.Modal(document.getElementById('bookingModal')).show();
    }

    updateTotalAmount() {
        const tripId = document.getElementById('selectedTripId').value;
        const seatCount = parseInt(document.getElementById('seatCount').value) || 1;
        
        const trip = this.currentTrips.find(t => t.id == tripId);
        if (trip) {
            const total = trip.price * seatCount;
            document.getElementById('totalAmount').textContent = new Intl.NumberFormat('fr-FR').format(total);
        }
    }

    async confirmBooking() {
        const form = document.getElementById('bookingForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/bookings/create/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();
                this.showSuccess('Réservation créée avec succès!');
                
                // Recharger les données
                await this.loadAvailableTrips();
                await this.loadMyBookings();
                
                // Naviguer vers les réservations
                this.showSection('mes-reservations');
            } else {
                this.showError('Erreur: ' + result.message);
            }
        } catch (error) {
            console.error('Erreur création réservation:', error);
            this.showError('Erreur lors de la création de la réservation');
        }
    }

    filterTrips(filter) {
        let filteredTrips = this.currentTrips;
        const now = new Date();

        if (filter === 'today') {
            const today = now.toISOString().split('T')[0];
            filteredTrips = filteredTrips.filter(trip => {
                const tripDate = new Date(trip.departure_time).toISOString().split('T')[0];
                return tripDate === today;
            });
        } else if (filter === 'tomorrow') {
            const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000).toISOString().split('T')[0];
            filteredTrips = filteredTrips.filter(trip => {
                const tripDate = new Date(trip.departure_time).toISOString().split('T')[0];
                return tripDate === tomorrow;
            });
        }

        this.displayTrips(filteredTrips);

        // Marquer le bouton actif
        document.querySelectorAll('.btn-group .btn').forEach(btn => {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-primary');
        });
        event.target.classList.remove('btn-outline-primary');
        event.target.classList.add('btn-primary');
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showAlert(message, type = 'info') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show position-fixed" style="top: 20px; right: 20px; z-index: 9999;">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-remove après 5 secondes
        setTimeout(() => {
            const alert = document.querySelector('.alert');
            if (alert) alert.remove();
        }, 5000);
    }

    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        window.location.href = '/auth/login/';
    }
}

// Fonctions globales
window.showBookingModal = function(tripId) {
    window.client.showBookingModal(tripId);
};

window.confirmBooking = function() {
    window.client.confirmBooking();
};

window.filterTrips = function(filter) {
    window.client.filterTrips(filter);
};

window.viewBookingDetails = function(bookingNumber) {
    alert('Détails de la réservation en cours de développement');
};

window.downloadTicket = function(bookingNumber) {
    alert('Téléchargement du ticket en cours de développement');
};

window.cancelBooking = function(bookingNumber) {
    if (confirm('Êtes-vous sûr de vouloir annuler cette réservation?')) {
        alert('Annulation en cours de développement');
    }
};

window.logout = function() {
    window.client.logout();
};

// Initialiser l'application
document.addEventListener('DOMContentLoaded', () => {
    window.client = new ClientDashboard();
});