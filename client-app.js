// Client Application JavaScript - XAF uniquement avec Authentification
class TravelApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8009';
        this.token = localStorage.getItem('authToken');
        this.user = JSON.parse(localStorage.getItem('userInfo') || 'null');
        this.currency = 'XAF';  // Franc CFA uniquement
        this.init();
    }

    init() {
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

        this.setupEventListeners();
        this.loadUserProfile();
        this.displayUserInfo();
    }

    redirectToLogin() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        window.location.href = '/auth/login/';
    }

    async loadUserProfile() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/profile/`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (!response.ok) {
                this.redirectToLogin();
                return;
            }

            const userData = await response.json();
            this.user = userData;
            localStorage.setItem('userInfo', JSON.stringify(userData));
            this.displayUserInfo();

        } catch (error) {
            console.error('Erreur chargement profil:', error);
            this.redirectToLogin();
        }
    }

    displayUserInfo() {
        // Afficher les informations utilisateur dans l'interface
        const userInfoElements = document.querySelectorAll('.user-name');
        userInfoElements.forEach(el => {
            el.textContent = `${this.user.first_name} ${this.user.last_name}`;
        });

        const userEmailElements = document.querySelectorAll('.user-email');
        userEmailElements.forEach(el => {
            el.textContent = this.user.email;
        });

        // Pré-remplir le numéro Orange Money si disponible
        if (this.user.orange_money) {
            const orangePhoneInput = document.getElementById('orangePhone');
            if (orangePhoneInput) {
                orangePhoneInput.value = this.user.orange_money;
            }
        }

        // Pré-remplir les informations de réservation
        const passengerNameInput = document.getElementById('passengerName');
        const passengerEmailInput = document.getElementById('passengerEmail');
        const passengerPhoneInput = document.getElementById('passengerPhone');

        if (passengerNameInput) {
            passengerNameInput.value = `${this.user.first_name} ${this.user.last_name}`;
        }
        if (passengerEmailInput) {
            passengerEmailInput.value = this.user.email;
        }
        if (passengerPhoneInput) {
            passengerPhoneInput.value = this.user.phone;
        }
    }

    logout() {
        // Appeler l'API de déconnexion
        fetch(`${this.apiBaseUrl}/auth/logout/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });

        // Nettoyer le stockage local
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        
        // Rediriger vers la page de connexion
        window.location.href = '/auth/login/';
    }

    // ...existing code...

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
        this.setMinDate();
    }

    setupEventListeners() {
        // Search form
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchTrips();
        });

        // Login form
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        // Register form
        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });
    }

    setMinDate() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('departureDate').min = today;
    }

    async checkAuthStatus() {
        if (this.token) {
            try {
                const response = await fetch(`${this.apiBaseUrl}/auth/profile/`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    this.user = await response.json();
                    this.showUserInterface();
                } else {
                    this.logout();
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                this.logout();
            }
        }
    }

    showUserInterface() {
        document.getElementById('authButtons').classList.add('d-none');
        document.getElementById('userMenu').classList.remove('d-none');
        document.getElementById('userName').textContent = this.user.first_name || this.user.username;
    }

    showLoginModal() {
        const modal = new bootstrap.Modal(document.getElementById('loginModal'));
        modal.show();
    }

    showRegisterModal() {
        const modal = new bootstrap.Modal(document.getElementById('registerModal'));
        modal.show();
    }

    async login() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('authToken', this.token);
                
                bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
                this.showUserInterface();
                this.showAlert('Connexion réussie !', 'success');
            } else {
                this.showAlert('Erreur de connexion. Vérifiez vos identifiants.', 'danger');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showAlert('Erreur de connexion au serveur.', 'danger');
        }
    }

    async register() {
        const formData = {
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            email: document.getElementById('email').value,
            username: document.getElementById('username').value,
            phone_number: document.getElementById('phone').value,
            password: document.getElementById('password').value,
            password_confirm: document.getElementById('passwordConfirm').value,
            role: 'client'
        };

        if (formData.password !== formData.password_confirm) {
            this.showAlert('Les mots de passe ne correspondent pas.', 'danger');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('authToken', this.token);
                
                bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
                this.showUserInterface();
                this.showAlert('Inscription réussie ! Bienvenue !', 'success');
            } else {
                const errors = Object.values(data).flat().join(' ');
                this.showAlert(errors || 'Erreur lors de l\'inscription.', 'danger');
            }
        } catch (error) {
            console.error('Register error:', error);
            this.showAlert('Erreur de connexion au serveur.', 'danger');
        }
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('authToken');
        
        document.getElementById('authButtons').classList.remove('d-none');
        document.getElementById('userMenu').classList.add('d-none');
        
        this.showAlert('Déconnexion réussie.', 'info');
    }

    async searchTrips() {
        const departure = document.getElementById('departureCity').value;
        const arrival = document.getElementById('arrivalCity').value;
        const date = document.getElementById('departureDate').value;
        const passengers = document.getElementById('passengers').value;

        if (departure === arrival) {
            this.showAlert('Les villes de départ et d\'arrivée ne peuvent pas être identiques.', 'warning');
            return;
        }

        // Simulation de données pour la démonstration
        const mockTrips = this.generateMockTrips(departure, arrival, date);
        this.displaySearchResults(mockTrips);
    }

    generateMockTrips(departure, arrival, date) {
        const cityNames = {
            'paris': 'Paris',
            'lyon': 'Lyon',
            'marseille': 'Marseille',
            'toulouse': 'Toulouse',
            'nice': 'Nice'
        };

        const trips = [];
        const basePrice = 25;
        const distances = {
            'paris-lyon': 462,
            'paris-marseille': 775,
            'lyon-nice': 472,
            'toulouse-paris': 680
        };

        for (let i = 0; i < 3; i++) {
            const departureTime = new Date(date);
            departureTime.setHours(8 + i * 4, 0, 0, 0);
            
            const distance = distances[`${departure}-${arrival}`] || 400;
            const duration = Math.round(distance / 80); // 80 km/h average
            
            const arrivalTime = new Date(departureTime);
            arrivalTime.setHours(arrivalTime.getHours() + duration);

            trips.push({
                id: `trip_${i + 1}`,
                route: {
                    departure_city: cityNames[departure],
                    arrival_city: cityNames[arrival]
                },
                departure_time: departureTime.toISOString(),
                arrival_time: arrivalTime.toISOString(),
                price: basePrice + (i * 5),
                available_seats: 45 - (i * 8),
                vehicle: {
                    registration_number: `TRK-00${i + 1}`,
                    brand: ['Renault', 'Mercedes', 'Volvo'][i],
                    model: ['Master', 'Sprinter', 'B11R'][i],
                    has_ac: true,
                    has_wifi: i > 0,
                    has_entertainment: i === 2
                },
                driver: {
                    user: {
                        first_name: ['Emmanuel', 'Ayina', 'Syntyche'][i],
                        last_name: ['Arthur', 'Kone', 'Mballa'][i]
                    }
                }
            });
        }

        return trips;
    }

    displaySearchResults(trips) {
        const resultsSection = document.getElementById('searchResults');
        const tripsList = document.getElementById('tripsList');
        
        if (trips.length === 0) {
            tripsList.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    Aucun voyage trouvé pour ces critères.
                </div>
            `;
        } else {
            tripsList.innerHTML = trips.map(trip => this.createTripCard(trip)).join('');
        }
        
        resultsSection.classList.remove('d-none');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    createTripCard(trip) {
        const departureTime = new Date(trip.departure_time);
        const arrivalTime = new Date(trip.arrival_time);
        
        const features = [];
        if (trip.vehicle.has_ac) features.push('<i class="fas fa-snowflake text-info" title="Climatisation"></i>');
        if (trip.vehicle.has_wifi) features.push('<i class="fas fa-wifi text-success" title="WiFi"></i>');
        if (trip.vehicle.has_entertainment) features.push('<i class="fas fa-tv text-primary" title="Divertissement"></i>');

        return `
            <div class="card mb-3 shadow-sm">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-3">
                            <div class="d-flex align-items-center">
                                <div class="text-center">
                                    <h5 class="mb-0">${departureTime.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</h5>
                                    <small class="text-muted">${trip.route.departure_city}</small>
                                </div>
                                <div class="mx-3">
                                    <i class="fas fa-arrow-right text-primary"></i>
                                </div>
                                <div class="text-center">
                                    <h5 class="mb-0">${arrivalTime.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</h5>
                                    <small class="text-muted">${trip.route.arrival_city}</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <p class="mb-1"><strong>Véhicule:</strong> ${trip.vehicle.brand} ${trip.vehicle.model}</p>
                            <p class="mb-1"><strong>Chauffeur:</strong> ${trip.driver.user.first_name} ${trip.driver.user.last_name}</p>
                            <div class="features">${features.join(' ')}</div>
                        </div>
                        <div class="col-md-2">
                            <p class="mb-1"><strong>Places disponibles:</strong></p>
                            <span class="badge ${trip.available_seats > 10 ? 'bg-success' : trip.available_seats > 5 ? 'bg-warning' : 'bg-danger'}">
                                ${trip.available_seats} places
                            </span>
                        </div>
                        <div class="col-md-2">
                            <h4 class="text-primary mb-0">${trip.price}€</h4>
                            <small class="text-muted">par personne</small>
                        </div>
                        <div class="col-md-2">
                            <button class="btn btn-primary w-100" onclick="app.showBookingModal('${trip.id}')" ${!this.token ? 'disabled title="Connexion requise"' : ''}>
                                <i class="fas fa-ticket-alt me-1"></i>
                                Réserver
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    showBookingModal(tripId) {
        if (!this.token) {
            this.showAlert('Veuillez vous connecter pour effectuer une réservation.', 'warning');
            return;
        }

        // Simulation des données du voyage
        const trip = this.getMockTripById(tripId);
        
        const bookingContent = document.getElementById('bookingContent');
        bookingContent.innerHTML = `
            <div class="trip-summary bg-light p-3 rounded mb-4">
                <h6>Résumé du voyage</h6>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Trajet:</strong> ${trip.route.departure_city} → ${trip.route.arrival_city}</p>
                        <p><strong>Date:</strong> ${new Date(trip.departure_time).toLocaleDateString('fr-FR')}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Heure:</strong> ${new Date(trip.departure_time).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })} - ${new Date(trip.arrival_time).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</p>
                        <p><strong>Prix:</strong> ${trip.price}€ par personne</p>
                    </div>
                </div>
            </div>
            
            <form id="bookingForm">
                <input type="hidden" id="tripId" value="${tripId}">
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Nom du passager</label>
                        <input type="text" class="form-control" id="passengerName" value="${this.user.first_name} ${this.user.last_name}" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Téléphone</label>
                        <input type="tel" class="form-control" id="passengerPhone" value="${this.user.phone_number || ''}" required>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" class="form-control" id="passengerEmail" value="${this.user.email}" required>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Nombre de places</label>
                    <select class="form-select" id="seatCount" onchange="app.updateBookingTotal()">
                        <option value="1">1 place</option>
                        <option value="2">2 places</option>
                        <option value="3">3 places</option>
                        <option value="4">4 places</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Méthode de paiement</label>
                    <select class="form-select" id="paymentMethod" required>
                        <option value="">Sélectionner...</option>
                        <option value="card">Carte bancaire</option>
                        <option value="mobile">Mobile Money</option>
                        <option value="cash">Espèces (à bord)</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Demandes spéciales (optionnel)</label>
                    <textarea class="form-control" id="specialRequests" rows="3" placeholder="Siège côté fenêtre, assistance mobilité, etc."></textarea>
                </div>
                
                <div class="booking-total bg-primary text-white p-3 rounded mb-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <span><strong>Total à payer:</strong></span>
                        <span class="h4 mb-0" id="totalAmount">${trip.price}€</span>
                    </div>
                </div>
                
                <div class="d-grid">
                    <button type="submit" class="btn btn-success btn-lg">
                        <i class="fas fa-credit-card me-2"></i>
                        Confirmer la Réservation
                    </button>
                </div>
            </form>
        `;

        // Setup booking form submission
        document.getElementById('bookingForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitBooking();
        });

        const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
        modal.show();
    }

    updateBookingTotal() {
        const seatCount = parseInt(document.getElementById('seatCount').value);
        const basePrice = 25; // Récupérer le prix réel du voyage
        const total = basePrice * seatCount;
        document.getElementById('totalAmount').textContent = `${total}€`;
    }

    async submitBooking() {
        const bookingData = {
            trip_id: document.getElementById('tripId').value,
            passenger_name: document.getElementById('passengerName').value,
            passenger_phone: document.getElementById('passengerPhone').value,
            passenger_email: document.getElementById('passengerEmail').value,
            seat_count: document.getElementById('seatCount').value,
            payment_method: document.getElementById('paymentMethod').value,
            special_requests: document.getElementById('specialRequests').value,
            total_amount: this.calculateTotalAmount()
        };

        try {
            // Étape 1: Traiter le paiement
            const paymentResult = await this.processPayment(bookingData);
            
            if (paymentResult.status === 'success') {
                // Étape 2: Créer la réservation
                const response = await fetch(`${this.apiBaseUrl}/bookings/booking/create/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': this.token ? `Bearer ${this.token}` : ''
                    },
                    body: JSON.stringify({
                        ...bookingData,
                        payment_id: paymentResult.payment_id
                    })
                });

                const result = await response.json();
                
                if (response.ok) {
                    bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();
                    this.showBookingConfirmation(result.booking_number, bookingData, paymentResult);
                    this.showAlert(`Réservation confirmée ! Numéro: ${result.booking_number}`, 'success');
                } else {
                    this.showAlert('Erreur lors de la réservation: ' + result.message, 'danger');
                }
            } else {
                this.showAlert('Erreur de paiement: ' + paymentResult.message, 'danger');
            }
            
        } catch (error) {
            console.error('Booking error:', error);
            this.showAlert('Erreur lors de la réservation. Veuillez réessayer.', 'danger');
        }
    }

    async processPayment(bookingData) {
        const paymentData = {
            amount: bookingData.total_amount,
            currency: 'EUR',
            payment_method: bookingData.payment_method,
            description: `Voyage ${bookingData.passenger_name} - ${bookingData.seat_count} place(s)`
        };

        try {
            const response = await fetch(`${this.apiBaseUrl}/payment/process/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(paymentData)
            });

            return await response.json();
        } catch (error) {
            console.error('Payment error:', error);
            return { status: 'error', message: 'Erreur de connexion au service de paiement' };
        }
    }

    calculateTotalAmount() {
        const seatCount = parseInt(document.getElementById('seatCount')?.value || 1);
        const selectedTrip = this.selectedTrip;
        
        if (!selectedTrip) return 0;
        
        // Prix de base en XAF
        const basePrice = selectedTrip.price || 15000;
        const subtotal = basePrice * seatCount;
        
        // Frais selon la méthode de paiement
        const paymentMethod = document.getElementById('paymentMethod')?.value;
        let fees = 0;
        
        if (paymentMethod === 'orange_money') {
            fees = Math.max(100, subtotal * 0.015); // 1.5% avec minimum 100 XAF
        }
        
        return Math.round(subtotal + fees);
    }

    showBookingConfirmation(bookingNumber, bookingData) {
        // Créer une modal de confirmation personnalisée
        const confirmationModal = `
            <div class="modal fade" id="confirmationModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header bg-success text-white">
                            <h5 class="modal-title">
                                <i class="fas fa-check-circle me-2"></i>Réservation Confirmée
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <div class="mb-4">
                                <i class="fas fa-ticket-alt fa-3x text-success mb-3"></i>
                                <h4>Réservation réussie !</h4>
                                <p class="lead">Numéro de réservation: <strong>${bookingNumber}</strong></p>
                            </div>
                            <div class="alert alert-info">
                                <p class="mb-0"><strong>Important:</strong> Présentez-vous 15 minutes avant le départ avec une pièce d'identité.</p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" onclick="app.downloadTicket('${bookingNumber}')">
                                <i class="fas fa-download me-2"></i>Télécharger le Billet
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', confirmationModal);
        const modal = new bootstrap.Modal(document.getElementById('confirmationModal'));
        modal.show();
    }

    downloadTicket(bookingNumber) {
        // Simulation du téléchargement de billet
        this.showAlert('Téléchargement du billet en cours...', 'info');
    }

    getMockTripById(tripId) {
        // Retourner des données de voyage simulées
        return {
            id: tripId,
            route: {
                departure_city: 'Paris',
                arrival_city: 'Lyon'
            },
            departure_time: new Date().toISOString(),
            arrival_time: new Date(Date.now() + 4 * 60 * 60 * 1000).toISOString(),
            price: 25
        };
    }

    searchDestination(city) {
        // Scroll to search section and pre-fill destination
        document.getElementById('arrivalCity').value = city;
        document.getElementById('search').scrollIntoView({ behavior: 'smooth' });
    }

    scrollToSearch() {
        document.getElementById('search').scrollIntoView({ behavior: 'smooth' });
    }

    showDestinations() {
        document.getElementById('destinations').scrollIntoView({ behavior: 'smooth' });
    }

    showProfile() {
        this.showAlert('Fonction de profil en cours de développement.', 'info');
    }

    showMyBookings() {
        this.showAlert('Fonction de mes réservations en cours de développement.', 'info');
    }

    showAlert(message, type) {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertContainer);
        
        setTimeout(() => {
            if (alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    }
}

// Global functions for inline event handlers
window.showLoginModal = () => app.showLoginModal();
window.showRegisterModal = () => app.showRegisterModal();
window.logout = () => app.logout();
window.showProfile = () => app.showProfile();
window.showMyBookings = () => app.showMyBookings();
window.scrollToSearch = () => app.scrollToSearch();
window.showDestinations = () => app.showDestinations();
window.searchDestination = (city) => app.searchDestination(city);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TravelApp();
});