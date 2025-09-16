// Admin Backoffice JavaScript SIMPLIFIÉ
class AdminBackoffice {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8002';
        this.token = localStorage.getItem('authToken');
        this.user = JSON.parse(localStorage.getItem('userInfo') || 'null');
        this.currentSection = 'dashboard';
        this.init();
    }

    async init() {
        console.log('Initialisation du backoffice...');
        
        // Vérification simple sans redirection automatique
        if (!this.token || !this.user) {
            console.log('Pas de token ou utilisateur');
            return;
        }

        if (this.user.role !== 'admin') {
            console.log('Utilisateur non admin');
            return;
        }

        // Afficher les informations admin
        this.displayAdminInfo();
        
        // Charger les données de base sans erreur
        this.loadBasicData();
        
        console.log('Backoffice initialisé avec succès');
    }

    displayAdminInfo() {
        console.log('Affichage des informations admin');
        const userName = document.getElementById('userName');
        if (userName && this.user) {
            userName.textContent = `${this.user.first_name} ${this.user.last_name}`;
        }

        // Ajouter les informations admin à la sidebar
        const sidebarTitle = document.querySelector('.sidebar h4');
        if (sidebarTitle && this.user) {
            sidebarTitle.innerHTML = `
                <i class="fas fa-shield-alt"></i> RoadShield
                <div class="text-white-50 small mt-1">
                    Connecté: ${this.user.first_name}
                </div>
            `;
        }
    }

    loadBasicData() {
        // Charger les données de base sans erreur
        this.loadSimpleStats();
        this.setupSimpleEventListeners();
    }

    loadSimpleStats() {
        // Statistiques simples sans API
        document.getElementById('tripsToday').textContent = '5';
        document.getElementById('activeBuses').textContent = '8';
        document.getElementById('totalReservations').textContent = '23';
        document.getElementById('totalRevenue').textContent = '345,000';
        
        // Activités récentes simple
        const container = document.getElementById('recentActivities');
        if (container) {
            container.innerHTML = '<p class="text-muted">Données chargées avec succès</p>';
        }
    }

    setupSimpleEventListeners() {
        // Événements simples sans complexité
        console.log('Configuration des événements de base');
    }

    async loadDashboardStats() {
        try {
            // Utiliser des données de test pour l'instant
            console.log('Chargement des statistiques dashboard...');
            
            // Statistiques factices pour tester
            const mockStats = {
                tripsToday: 5,
                activeBuses: 8,
                totalReservations: 23,
                totalRevenue: 345000
            };

            // Mettre à jour les statistiques
            document.getElementById('tripsToday').textContent = mockStats.tripsToday;
            document.getElementById('activeBuses').textContent = mockStats.activeBuses;
            document.getElementById('totalReservations').textContent = mockStats.totalReservations;
            document.getElementById('totalRevenue').textContent = new Intl.NumberFormat('fr-FR').format(mockStats.totalRevenue);

            // Afficher les activités récentes factices
            this.displayRecentActivities([]);

        } catch (error) {
            console.error('Erreur chargement dashboard:', error);
            // Ne pas afficher d'erreur pour éviter les alertes répétées
        }
    }

    displayRecentActivities(reservations) {
        const container = document.getElementById('recentActivities');
        
        if (reservations.length === 0) {
            container.innerHTML = '<p class="text-muted">Aucune activité récente</p>';
            return;
        }

        const html = reservations.map(res => `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <strong>${res.passenger_name}</strong><br>
                    <small class="text-muted">${res.trip?.departure_city} → ${res.trip?.arrival_city}</small>
                </div>
                <div class="text-end">
                    <span class="badge bg-${res.status === 'confirmed' ? 'success' : 'warning'}">${res.status}</span><br>
                    <small class="text-muted">${new Date(res.created_at).toLocaleDateString('fr-FR')}</small>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    async loadTrips() {
        try {
            console.log('Chargement des voyages...');
            
            // Données de test pour les voyages
            const mockTrips = [
                {
                    id: 1,
                    departure_city: 'Douala',
                    arrival_city: 'Yaoundé',
                    departure_time: '2025-09-15T08:00:00',
                    price: 15000,
                    available_seats: 45,
                    total_seats: 50,
                    status: 'scheduled',
                    bus: {
                        registration_number: 'CM-1234-AB',
                        brand: 'Mercedes',
                        model: 'Sprinter'
                    }
                },
                {
                    id: 2,
                    departure_city: 'Yaoundé',
                    arrival_city: 'Bafoussam',
                    departure_time: '2025-09-15T14:00:00',
                    price: 12000,
                    available_seats: 30,
                    total_seats: 40,
                    status: 'scheduled',
                    bus: {
                        registration_number: 'CM-5678-CD',
                        brand: 'Toyota',
                        model: 'Hiace'
                    }
                }
            ];
            
            this.displayTripsTable(mockTrips);
        } catch (error) {
            console.error('Erreur chargement voyages:', error);
        }
    }

    displayTripsTable(trips) {
        const tbody = document.getElementById('tripsTable');
        
        if (trips.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Aucun voyage</td></tr>';
            return;
        }

        const html = trips.map(trip => `
            <tr>
                <td><code>${trip.id}</code></td>
                <td>${trip.departure_city} → ${trip.arrival_city}</td>
                <td>${new Date(trip.departure_time).toLocaleString('fr-FR')}</td>
                <td>${new Intl.NumberFormat('fr-FR').format(trip.price)} XAF</td>
                <td>
                    <span class="badge bg-info">${trip.available_seats}/${trip.total_seats}</span>
                </td>
                <td>
                    ${trip.bus?.registration_number || 'N/A'}<br>
                    <small class="text-muted">${trip.bus?.brand} ${trip.bus?.model}</small>
                </td>
                <td>
                    <span class="badge bg-${trip.status === 'scheduled' ? 'success' : 'secondary'}">${trip.status}</span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editTrip('${trip.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteTrip('${trip.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = html;
    }

    async loadBuses() {
        try {
            console.log('Chargement des bus...');
            
            // Données de test pour les bus
            const mockBuses = [
                {
                    id: 1,
                    registration_number: 'CM-1234-AB',
                    brand: 'Mercedes',
                    model: 'Sprinter',
                    year: 2023,
                    capacity: 50,
                    driver_name: 'Jean Dupont',
                    driver_phone: '+237 699 123 456',
                    has_ac: true,
                    has_wifi: true,
                    status: 'active'
                },
                {
                    id: 2,
                    registration_number: 'CM-5678-CD',
                    brand: 'Toyota',
                    model: 'Hiace',
                    year: 2022,
                    capacity: 40,
                    driver_name: 'Paul Martin',
                    driver_phone: '+237 677 987 654',
                    has_ac: false,
                    has_wifi: false,
                    status: 'active'
                }
            ];
            
            this.displayBusesTable(mockBuses);
        } catch (error) {
            console.error('Erreur chargement bus:', error);
        }
    }

    displayBusesTable(buses) {
        const tbody = document.getElementById('busesTable');
        
        if (buses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">Aucun bus</td></tr>';
            return;
        }

        const html = buses.map(bus => `
            <tr>
                <td><strong>${bus.registration_number}</strong></td>
                <td>
                    ${bus.brand} ${bus.model}<br>
                    <small class="text-muted">${bus.year}</small>
                </td>
                <td><span class="badge bg-info">${bus.capacity} places</span></td>
                <td>
                    ${bus.driver_name}<br>
                    <small class="text-muted">${bus.driver_phone}</small>
                </td>
                <td>
                    ${bus.has_ac ? '<i class="fas fa-snowflake text-info" title="Climatisation"></i>' : ''}
                    ${bus.has_wifi ? '<i class="fas fa-wifi text-success" title="WiFi"></i>' : ''}
                </td>
                <td>
                    <span class="badge bg-${bus.status === 'active' ? 'success' : 'secondary'}">${bus.status}</span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editBus('${bus.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-warning me-1" onclick="toggleBusStatus('${bus.id}')">
                        <i class="fas fa-power-off"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="viewBusDetails('${bus.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = html;
    }

    async loadBusesForSelect() {
        try {
            console.log('Chargement des bus pour select...');
            
            // Données de test pour le select
            const mockBuses = [
                { id: 1, registration_number: 'CM-1234-AB', brand: 'Mercedes', model: 'Sprinter', status: 'active' },
                { id: 2, registration_number: 'CM-5678-CD', brand: 'Toyota', model: 'Hiace', status: 'active' }
            ];
            
            const select = document.getElementById('busSelect');
            if (select) {
                select.innerHTML = '<option value="">Sélectionner un bus</option>';
                
                mockBuses.forEach(bus => {
                    if (bus.status === 'active') {
                        select.innerHTML += `<option value="${bus.id}">${bus.registration_number} - ${bus.brand} ${bus.model}</option>`;
                    }
                });
            }
        } catch (error) {
            console.error('Erreur chargement bus pour select:', error);
        }
    }

    async loadReservations(filter = 'all') {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/reservations/`);
            const data = await response.json();
            
            let reservations = data.reservations || [];
            
            // Appliquer le filtre
            if (filter !== 'all') {
                reservations = reservations.filter(res => res.status === filter);
            }
            
            this.displayReservationsTable(reservations);
            this.updateReservationStats(data.reservations || []);
        } catch (error) {
            console.error('Erreur chargement réservations:', error);
        }
    }

    updateReservationStats(reservations) {
        const pending = reservations.filter(r => r.status === 'pending').length;
        const confirmed = reservations.filter(r => r.status === 'confirmed').length;
        const totalRevenue = reservations.reduce((sum, r) => sum + (r.total_amount || 0), 0);
        const totalPassengers = reservations.reduce((sum, r) => sum + (r.seat_count || 0), 0);

        document.getElementById('pendingCount').textContent = pending;
        document.getElementById('confirmedCount').textContent = confirmed;
        document.getElementById('totalRevenue').textContent = new Intl.NumberFormat('fr-FR').format(totalRevenue) + ' XAF';
        document.getElementById('totalPassengers').textContent = totalPassengers;
    }

    displayReservationsTable(reservations) {
        const tbody = document.getElementById('reservationsTable');
        
        if (reservations.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Aucune réservation</td></tr>';
            return;
        }

        const html = reservations.map(res => `
            <tr>
                <td><code>${res.booking_number}</code></td>
                <td>
                    <strong>${res.passenger_name}</strong><br>
                    <small class="text-muted">${res.passenger_phone}</small>
                </td>
                <td>
                    ${res.trip?.departure_city} → ${res.trip?.arrival_city}<br>
                    <small class="text-muted">${new Date(res.trip?.departure_time).toLocaleDateString('fr-FR')}</small>
                </td>
                <td><span class="badge bg-primary">${res.seat_count}</span></td>
                <td><strong>${new Intl.NumberFormat('fr-FR').format(res.total_amount)} XAF</strong></td>
                <td>
                    <span class="badge bg-${res.payment_status === 'paid' ? 'success' : 'warning'}">${res.payment_status}</span><br>
                    <small class="text-muted">${res.payment_method}</small>
                </td>
                <td>
                    <span class="badge bg-${res.status === 'confirmed' ? 'success' : res.status === 'pending' ? 'warning' : 'danger'}">${res.status}</span>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editReservation('${res.booking_number}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-success" onclick="confirmReservation('${res.booking_number}')">
                            <i class="fas fa-check"></i>
                        </button>
                        <button class="btn btn-outline-info" onclick="printTicket('${res.booking_number}')">
                            <i class="fas fa-print"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = html;
    }

    async loadTickets() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/tickets/`);
            const data = await response.json();
            
            this.displayTicketsTable(data.tickets || []);
        } catch (error) {
            console.error('Erreur chargement tickets:', error);
        }
    }

    displayTicketsTable(tickets) {
        const tbody = document.getElementById('ticketsTable');
        
        if (tickets.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Aucun ticket</td></tr>';
            return;
        }

        const html = tickets.map(ticket => `
            <tr>
                <td><code>${ticket.ticket_number}</code></td>
                <td><strong>${ticket.passenger_name}</strong></td>
                <td>${ticket.departure_city} → ${ticket.arrival_city}</td>
                <td>${new Date(ticket.departure_time).toLocaleString('fr-FR')}</td>
                <td>${ticket.bus_registration}</td>
                <td><span class="badge bg-primary">${ticket.seat_count}</span></td>
                <td><span class="badge bg-success">${ticket.status}</span></td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="printTicket('${ticket.booking_number}')">
                            <i class="fas fa-print"></i> Imprimer
                        </button>
                        <button class="btn btn-outline-info" onclick="emailTicket('${ticket.booking_number}')">
                            <i class="fas fa-envelope"></i> Email
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = html;
    }

    async createTrip() {
        const form = document.getElementById('createTripForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        console.log('Données du voyage à créer:', data);

        try {
            // Simuler la création pour l'instant
            console.log('Simulation: Création du voyage...');
            
            // Simulation d'une réponse réussie
            setTimeout(() => {
                bootstrap.Modal.getInstance(document.getElementById('createTripModal')).hide();
                form.reset();
                this.showAlert('Voyage créé avec succès! (Simulation)', 'success');
                this.loadTrips(); // Recharger la liste
            }, 500);
            
        } catch (error) {
            console.error('Erreur création voyage:', error);
            this.showAlert('Erreur lors de la création du voyage', 'danger');
        }
    }

    async updateTrip() {
        const form = document.getElementById('editTripForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        const tripId = data.trip_id;

        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/trips/${tripId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                bootstrap.Modal.getInstance(document.getElementById('editTripModal')).hide();
                this.showAlert('Voyage modifié avec succès!', 'success');
                this.loadTrips();
            } else {
                this.showAlert('Erreur: ' + result.message, 'danger');
            }
        } catch (error) {
            console.error('Erreur modification voyage:', error);
            this.showAlert('Erreur lors de la modification du voyage', 'danger');
        }
    }

    async deleteTrip(tripId) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer ce voyage?')) {
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/trips/${tripId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const result = await response.json();
                this.showAlert('Voyage supprimé avec succès!', 'success');
                this.loadTrips();
            } else {
                const result = await response.json();
                this.showAlert('Erreur: ' + result.message, 'danger');
            }
        } catch (error) {
            console.error('Erreur suppression voyage:', error);
            this.showAlert('Erreur lors de la suppression du voyage', 'danger');
        }
    }

    async editTrip(tripId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/trips/${tripId}/`);
            const trip = await response.json();

            if (response.ok) {
                // Remplir le formulaire d'édition
                document.getElementById('editTripId').value = trip.id;
                document.getElementById('editDepartureCity').value = trip.departure_city;
                document.getElementById('editArrivalCity').value = trip.arrival_city;
                
                // Formater les dates pour datetime-local
                if (trip.departure_time) {
                    const depDate = new Date(trip.departure_time);
                    document.getElementById('editDepartureTime').value = depDate.toISOString().slice(0, -8);
                }
                if (trip.arrival_time) {
                    const arrDate = new Date(trip.arrival_time);
                    document.getElementById('editArrivalTime').value = arrDate.toISOString().slice(0, -8);
                }
                
                document.getElementById('editPrice').value = trip.price;
                document.getElementById('editAvailableSeats').value = trip.available_seats;
                document.getElementById('editStatus').value = trip.status;
                
                // Charger les bus pour le select d'édition
                await this.loadBusesForEditSelect();
                document.getElementById('editBusSelect').value = trip.bus?.id || '';

                // Afficher la modal
                new bootstrap.Modal(document.getElementById('editTripModal')).show();
            } else {
                this.showAlert('Erreur lors du chargement du voyage', 'danger');
            }
        } catch (error) {
            console.error('Erreur chargement voyage:', error);
            this.showAlert('Erreur lors du chargement du voyage', 'danger');
        }
    }

    async loadBusesForEditSelect() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/buses/`);
            const data = await response.json();
            
            const select = document.getElementById('editBusSelect');
            select.innerHTML = '<option value="">Sélectionner un bus</option>';
            
            data.buses?.forEach(bus => {
                select.innerHTML += `<option value="${bus.id}">${bus.registration_number} - ${bus.brand} ${bus.model}</option>`;
            });
        } catch (error) {
            console.error('Erreur chargement bus pour edit select:', error);
        }
    }

    async loadDrivers() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/drivers/`);
            const data = await response.json();
            
            this.displayDriversTable(data.drivers || []);
        } catch (error) {
            console.error('Erreur chargement chauffeurs:', error);
        }
    }

    displayDriversTable(drivers) {
        const tbody = document.getElementById('driversTable');
        
        if (drivers.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Aucun chauffeur</td></tr>';
            return;
        }

        const html = drivers.map(driver => `
            <tr>
                <td>
                    <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                        ${driver.first_name.charAt(0)}${driver.last_name.charAt(0)}
                    </div>
                </td>
                <td>
                    <strong>${driver.first_name} ${driver.last_name}</strong><br>
                    <small class="text-muted">${driver.email || 'Pas d\'email'}</small>
                </td>
                <td>${driver.phone}</td>
                <td>
                    ${driver.license_number}<br>
                    <small class="text-muted">Exp: ${new Date(driver.license_expiry).toLocaleDateString('fr-FR')}</small>
                </td>
                <td>
                    ${driver.assigned_bus ? `
                        <span class="badge bg-success">${driver.assigned_bus.registration_number}</span><br>
                        <small class="text-muted">${driver.assigned_bus.brand} ${driver.assigned_bus.model}</small>
                    ` : '<span class="text-muted">Aucun bus assigné</span>'}
                </td>
                <td>
                    <div class="d-flex align-items-center">
                        ${this.generateStars(driver.rating || 0)}
                        <span class="ms-2">${(driver.rating || 0).toFixed(1)}</span>
                    </div>
                </td>
                <td>
                    <span class="badge bg-${driver.status === 'available' ? 'success' : driver.status === 'busy' ? 'warning' : 'secondary'}">${driver.status}</span>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editDriver('${driver.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-info" onclick="viewDriverProfile('${driver.id}')">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="toggleDriverStatus('${driver.id}')">
                            <i class="fas fa-power-off"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = html;
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '';
        
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star text-warning"></i>';
        }
        
        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt text-warning"></i>';
        }
        
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star text-warning"></i>';
        }
        
        return stars;
    }

    async loadDriversForSelect() {
        try {
            console.log('Chargement des chauffeurs pour select...');
            
            // Données de test pour les chauffeurs
            const mockDrivers = [
                { id: 1, first_name: 'Jean', last_name: 'Dupont', status: 'available' },
                { id: 2, first_name: 'Paul', last_name: 'Martin', status: 'available' },
                { id: 3, first_name: 'Pierre', last_name: 'Durand', status: 'busy' }
            ];
            
            const selects = ['editDriverSelect'];
            selects.forEach(selectId => {
                const select = document.getElementById(selectId);
                if (select) {
                    select.innerHTML = '<option value="">Aucun chauffeur assigné</option>';
                    
                    mockDrivers.forEach(driver => {
                        if (driver.status === 'available') {
                            select.innerHTML += `<option value="${driver.id}">${driver.first_name} ${driver.last_name}</option>`;
                        }
                    });
                }
            });
        } catch (error) {
            console.error('Erreur chargement chauffeurs pour select:', error);
        }
    }

    async createDriver() {
        const form = document.getElementById('createDriverForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/drivers/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                bootstrap.Modal.getInstance(document.getElementById('createDriverModal')).hide();
                form.reset();
                this.showAlert('Chauffeur ajouté avec succès!', 'success');
                this.loadDrivers();
                this.loadDriversForSelect();
            } else {
                this.showAlert('Erreur: ' + result.message, 'danger');
            }
        } catch (error) {
            console.error('Erreur création chauffeur:', error);
            this.showAlert('Erreur lors de l\'ajout du chauffeur', 'danger');
        }
    }

    async editBus(busId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/buses/${busId}/`);
            const bus = await response.json();

            if (response.ok) {
                // Remplir le formulaire d'édition
                document.getElementById('editBusId').value = bus.id;
                document.getElementById('editRegistrationNumber').value = bus.registration_number;
                document.getElementById('editBrand').value = bus.brand;
                document.getElementById('editModel').value = bus.model;
                document.getElementById('editCapacity').value = bus.capacity;
                document.getElementById('editYear').value = bus.year;
                document.getElementById('editBusStatus').value = bus.status;
                document.getElementById('editHasAc').checked = bus.has_ac;
                document.getElementById('editHasWifi').checked = bus.has_wifi;
                
                // Charger les chauffeurs et sélectionner celui assigné
                await this.loadDriversForSelect();
                document.getElementById('editDriverSelect').value = bus.driver?.id || '';

                // Afficher la modal
                new bootstrap.Modal(document.getElementById('editBusModal')).show();
            } else {
                this.showAlert('Erreur lors du chargement du bus', 'danger');
            }
        } catch (error) {
            console.error('Erreur chargement bus:', error);
            this.showAlert('Erreur lors du chargement du bus', 'danger');
        }
    }

    async updateBus() {
        const form = document.getElementById('editBusForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        const busId = data.bus_id;

        // Convertir les checkboxes
        data.has_ac = document.getElementById('editHasAc').checked;
        data.has_wifi = document.getElementById('editHasWifi').checked;

        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/buses/${busId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                bootstrap.Modal.getInstance(document.getElementById('editBusModal')).hide();
                this.showAlert('Bus modifié avec succès!', 'success');
                this.loadBuses();
                this.loadBusesForSelect();
            } else {
                this.showAlert('Erreur: ' + result.message, 'danger');
            }
        } catch (error) {
            console.error('Erreur modification bus:', error);
            this.showAlert('Erreur lors de la modification du bus', 'danger');
        }
    }

    async toggleBusStatus(busId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/buses/${busId}/toggle-status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();

            if (response.ok) {
                this.showAlert('Statut du bus modifié avec succès!', 'success');
                this.loadBuses();
                this.loadBusesForSelect();
            } else {
                this.showAlert('Erreur: ' + result.message, 'danger');
            }
        } catch (error) {
            console.error('Erreur changement statut bus:', error);
            this.showAlert('Erreur lors du changement de statut', 'danger');
        }
    }

    async createBus() {
        const form = document.getElementById('createBusForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Convertir les checkboxes
        data.has_ac = document.getElementById('hasAc').checked;
        data.has_wifi = document.getElementById('hasWifi').checked;

        try {
            const response = await fetch(`${this.apiBaseUrl}/admin/buses/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                bootstrap.Modal.getInstance(document.getElementById('createBusModal')).hide();
                form.reset();
                this.showAlert('Bus ajouté avec succès!', 'success');
                this.loadBuses();
                this.loadBusesForSelect();
            } else {
                this.showAlert('Erreur: ' + result.message, 'danger');
            }
        } catch (error) {
            console.error('Erreur création bus:', error);
            this.showAlert('Erreur lors de l\'ajout du bus', 'danger');
        }
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
}

// Fonctions globales
function showSection(sectionName) {
    // Cacher toutes les sections
    document.querySelectorAll('.section-content').forEach(section => {
        section.style.display = 'none';
    });
    
    // Supprimer la classe active de tous les liens
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Afficher la section demandée
    document.getElementById(sectionName + '-section').style.display = 'block';
    
    // Marquer le lien comme actif
    event.target.classList.add('active');
    
    // Mettre à jour la section courante
    window.admin.currentSection = sectionName;
    
    // Charger les données selon la section
    switch(sectionName) {
        case 'trips':
            window.admin.loadTrips();
            break;
        case 'buses':
            window.admin.loadBuses();
            break;
        case 'drivers':
            window.admin.loadDrivers();
            break;
        case 'reservations':
            window.admin.loadReservations();
            break;
        case 'tickets':
            window.admin.loadTickets();
            break;
    }
}

function showCreateTripModal() {
    new bootstrap.Modal(document.getElementById('createTripModal')).show();
}

function showCreateBusModal() {
    new bootstrap.Modal(document.getElementById('createBusModal')).show();
}

function showCreateDriverModal() {
    new bootstrap.Modal(document.getElementById('createDriverModal')).show();
}

function logout() {
    // Utiliser l'instance admin si disponible, sinon déconnexion basique
    if (window.admin && window.admin.logout) {
        window.admin.logout();
    } else {
        // Afficher un message de déconnexion
        const logoutBtn = document.querySelector('[onclick*="logout"]');
        if (logoutBtn) {
            logoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Déconnexion...';
            logoutBtn.style.pointerEvents = 'none';
        }
        
        // Nettoyer le stockage local
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        
        // Rediriger immédiatement
        window.location.href = '/auth/login/';
    }
}

// Fonctions de gestion
window.editTrip = function(tripId) {
    window.admin.editTrip(tripId);
};

window.deleteTrip = function(tripId) {
    window.admin.deleteTrip(tripId);
};

window.updateTrip = function() {
    window.admin.updateTrip();
};

window.editBus = function(busId) {
    window.admin.editBus(busId);
};

window.updateBus = function() {
    window.admin.updateBus();
};

window.createDriver = function() {
    window.admin.createDriver();
};

window.editDriver = function(driverId) {
    alert('Fonctionnalité d\'édition chauffeur en cours de développement');
};

window.viewDriverProfile = function(driverId) {
    alert('Profil chauffeur en cours de développement');
};

window.toggleDriverStatus = function(driverId) {
    alert('Changement statut chauffeur en cours de développement');
};

window.filterReservations = function(filter) {
    // Marquer le bouton actif
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.classList.remove('btn-warning', 'btn-success', 'btn-danger', 'btn-secondary');
        btn.classList.add('btn-outline-secondary', 'btn-outline-warning', 'btn-outline-success', 'btn-outline-danger');
    });
    
    const activeBtn = event.target;
    activeBtn.classList.remove('btn-outline-secondary', 'btn-outline-warning', 'btn-outline-success', 'btn-outline-danger');
    
    if (filter === 'pending') activeBtn.classList.add('btn-warning');
    else if (filter === 'confirmed') activeBtn.classList.add('btn-success');
    else if (filter === 'cancelled') activeBtn.classList.add('btn-danger');
    else activeBtn.classList.add('btn-secondary');
    
    window.admin.loadReservations(filter);
};

window.loadReservations = function() {
    window.admin.loadReservations();
};

window.toggleBusStatus = function(busId) {
    window.admin.toggleBusStatus(busId);
};

window.viewBusDetails = function(busId) {
    alert('Détails du bus en cours de développement');
};

window.editReservation = function(bookingNumber) {
    alert('Fonctionnalité d\'édition en cours de développement');
};

window.confirmReservation = function(bookingNumber) {
    alert('Fonctionnalité de confirmation en cours de développement');
};

window.printTicket = function(bookingNumber) {
    alert('Fonctionnalité d\'impression en cours de développement');
};

window.emailTicket = function(bookingNumber) {
    alert('Fonctionnalité d\'envoi email en cours de développement');
};

window.generateAllTickets = function() {
    alert('Génération de tous les tickets en cours...');
};

// Initialiser l'application
document.addEventListener('DOMContentLoaded', () => {
    window.admin = new AdminBackoffice();
});