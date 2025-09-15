// Admin Backoffice JavaScript ULTRA SIMPLIFIÉ

class AdminBackoffice {
    constructor() {
        this.user = JSON.parse(localStorage.getItem('userInfo') || 'null');
        this.init();
    }

    init() {
        console.log('Initialisation simple du backoffice...');
        
        // Afficher les informations de base
        if (this.user) {
            this.displayAdminInfo();
        }
        
        // Charger les statistiques de base
        this.loadSimpleStats();
        
        console.log('Backoffice initialisé');
    }

    displayAdminInfo() {
        const sidebarTitle = document.querySelector('.sidebar h4');
        if (sidebarTitle && this.user) {
            sidebarTitle.innerHTML = `
                <i class="fas fa-shield-alt"></i> RoadShield
                <div class="text-white-50 small mt-1">
                    Connecté: ${this.user.first_name || 'Admin'}
                </div>
            `;
        }
    }

    loadSimpleStats() {
        // Statistiques simples sans erreur
        if (document.getElementById('tripsToday')) {
            document.getElementById('tripsToday').textContent = '5';
        }
        if (document.getElementById('activeBuses')) {
            document.getElementById('activeBuses').textContent = '8';
        }
        if (document.getElementById('totalReservations')) {
            document.getElementById('totalReservations').textContent = '23';
        }
        if (document.getElementById('totalRevenue')) {
            document.getElementById('totalRevenue').textContent = '345,000';
        }
        
        const container = document.getElementById('recentActivities');
        if (container) {
            container.innerHTML = '<p class="text-muted">Système opérationnel</p>';
        }
    }

    // Fonctions de chargement simplifiées
    loadTrips() {
        const tbody = document.getElementById('tripsTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td>1</td>
                    <td>Douala → Yaoundé</td>
                    <td>15/09/2025 08:00</td>
                    <td>15,000 XAF</td>
                    <td><span class="badge bg-info">45/50</span></td>
                    <td>CM-1234-AB<br><small class="text-muted">Mercedes Sprinter</small></td>
                    <td><span class="badge bg-success">Programmé</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Yaoundé → Bafoussam</td>
                    <td>15/09/2025 14:00</td>
                    <td>12,000 XAF</td>
                    <td><span class="badge bg-info">30/40</span></td>
                    <td>CM-5678-CD<br><small class="text-muted">Toyota Hiace</small></td>
                    <td><span class="badge bg-success">Programmé</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    loadBuses() {
        const tbody = document.getElementById('busesTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td><strong>CM-1234-AB</strong></td>
                    <td>Mercedes Sprinter<br><small class="text-muted">2023</small></td>
                    <td><span class="badge bg-info">50 places</span></td>
                    <td>Jean Kamga<br><small class="text-muted">+237 699 123 456</small></td>
                    <td>
                        <i class="fas fa-snowflake text-info me-1" title="Climatisation"></i>
                        <i class="fas fa-wifi text-success me-1" title="WiFi"></i>
                        <i class="fas fa-plug text-warning" title="Prises USB"></i>
                    </td>
                    <td><span class="badge bg-success">🟢 Disponible</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info" title="Localiser">
                            <i class="fas fa-map-marker-alt"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td><strong>CM-5678-CD</strong></td>
                    <td>Volvo 9700<br><small class="text-muted">2022</small></td>
                    <td><span class="badge bg-info">65 places</span></td>
                    <td>Paul Nkomo<br><small class="text-muted">+237 677 987 654</small></td>
                    <td>
                        <i class="fas fa-snowflake text-info me-1" title="Climatisation"></i>
                        <i class="fas fa-wifi text-success me-1" title="WiFi"></i>
                        <i class="fas fa-restroom text-primary" title="Toilettes"></i>
                    </td>
                    <td><span class="badge bg-warning">🟡 En voyage</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-success" title="Suivre">
                            <i class="fas fa-route"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td><strong>CM-9012-EF</strong></td>
                    <td>Scania Touring<br><small class="text-muted">2024</small></td>
                    <td><span class="badge bg-info">55 places</span></td>
                    <td>Marie Tchinda<br><small class="text-muted">+237 655 111 222</small></td>
                    <td>
                        <i class="fas fa-snowflake text-info me-1" title="Climatisation"></i>
                        <i class="fas fa-wifi text-success me-1" title="WiFi"></i>
                        <i class="fas fa-plug text-warning me-1" title="Prises USB"></i>
                        <i class="fas fa-restroom text-primary" title="Toilettes"></i>
                    </td>
                    <td><span class="badge bg-danger">🔴 En panne</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" title="Signaler">
                            <i class="fas fa-exclamation-triangle"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td><strong>CM-3456-GH</strong></td>
                    <td>Mercedes Tourismo<br><small class="text-muted">2023</small></td>
                    <td><span class="badge bg-info">48 places</span></td>
                    <td>Non assigné<br><small class="text-muted">-</small></td>
                    <td>
                        <i class="fas fa-snowflake text-info me-1" title="Climatisation"></i>
                        <i class="fas fa-wifi text-success" title="WiFi"></i>
                    </td>
                    <td><span class="badge bg-secondary">🔧 En maintenance</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning" title="Maintenance">
                            <i class="fas fa-tools"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    loadDrivers() {
        const tbody = document.getElementById('driversTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td>
                        <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                            JD
                        </div>
                    </td>
                    <td><strong>Jean Dupont</strong><br><small class="text-muted">15 ans d'expérience</small></td>
                    <td>+237 699 123 456<br><small class="text-muted">j.dupont@roadshield.cm</small></td>
                    <td>CM-PERM-2023<br><small class="text-muted">Catégorie D</small></td>
                    <td><span class="badge bg-success">CM-1234-AB</span></td>
                    <td>⭐⭐⭐⭐⭐<br><small class="text-success">4.8/5</small></td>
                    <td><span class="badge bg-success">🟢 Actif</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info" title="Profil">
                            <i class="fas fa-user"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="bg-success text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                            MM
                        </div>
                    </td>
                    <td><strong>Marie Martin</strong><br><small class="text-muted">8 ans d'expérience</small></td>
                    <td>+237 677 987 654<br><small class="text-muted">m.martin@roadshield.cm</small></td>
                    <td>CM-PERM-2024<br><small class="text-muted">Catégorie D</small></td>
                    <td><span class="badge bg-warning">CM-5678-CD</span></td>
                    <td>⭐⭐⭐⭐☆<br><small class="text-warning">4.2/5</small></td>
                    <td><span class="badge bg-warning">🟡 En congé</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning" title="Congé">
                            <i class="fas fa-calendar-times"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="bg-info text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                            PB
                        </div>
                    </td>
                    <td><strong>Paul Bernard</strong><br><small class="text-muted">12 ans d'expérience</small></td>
                    <td>+237 655 111 222<br><small class="text-muted">p.bernard@roadshield.cm</small></td>
                    <td>CM-PERM-2022<br><small class="text-muted">Catégorie D+E</small></td>
                    <td><span class="badge bg-success">CM-9012-EF</span></td>
                    <td>⭐⭐⭐⭐⭐<br><small class="text-success">4.9/5</small></td>
                    <td><span class="badge bg-success">🟢 Actif</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-success" title="Excellent">
                            <i class="fas fa-star"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="bg-warning text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                            AS
                        </div>
                    </td>
                    <td><strong>Alice Simo</strong><br><small class="text-muted">6 ans d'expérience</small></td>
                    <td>+237 622 333 444<br><small class="text-muted">a.simo@roadshield.cm</small></td>
                    <td>CM-PERM-2025<br><small class="text-muted">Catégorie D1</small></td>
                    <td><span class="badge bg-secondary">Non assigné</span></td>
                    <td>⭐⭐⭐⭐☆<br><small class="text-primary">4.3/5</small></td>
                    <td><span class="badge bg-danger">🔴 Malade</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" title="Congé maladie">
                            <i class="fas fa-user-injured"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="bg-dark text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                            RN
                        </div>
                    </td>
                    <td><strong>Robert Ngono</strong><br><small class="text-muted">20 ans d'expérience</small></td>
                    <td>+237 688 555 666<br><small class="text-muted">r.ngono@roadshield.cm</small></td>
                    <td>CM-PERM-2020<br><small class="text-muted">Catégorie D</small></td>
                    <td><span class="badge bg-secondary">CM-3456-GH</span></td>
                    <td>⭐⭐⭐⭐⭐<br><small class="text-success">5.0/5</small></td>
                    <td><span class="badge bg-secondary">⚫ Suspendu</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-dark" title="Suspension">
                            <i class="fas fa-ban"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }
                    <td><span class="badge bg-success">Disponible</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    loadReservations() {
        const tbody = document.getElementById('reservationsTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td><code>RSV-001</code></td>
                    <td><strong>Pierre Martin</strong></td>
                    <td>Douala → Yaoundé</td>
                    <td><span class="badge bg-primary">2</span></td>
                    <td><strong>30,000 XAF</strong></td>
                    <td><span class="badge bg-success">Payé</span></td>
                    <td><span class="badge bg-success">Confirmé</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-print"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    loadTrips() {
        const tbody = document.getElementById('tripsTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td><strong>#001</strong></td>
                    <td>Douala → Yaoundé<br><small class="text-muted">248 km</small></td>
                    <td>15/09/2025 - 08:00<br><small class="text-muted">Durée: 4h</small></td>
                    <td><strong>5,000 XAF</strong></td>
                    <td><span class="badge bg-warning">45/50</span></td>
                    <td>CM-1234-AB<br><small class="text-muted">Jean Dupont</small></td>
                    <td><span class="badge bg-success">🟢 Programmé</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info" title="Détails">
                            <i class="fas fa-info"></i>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td><strong>#002</strong></td>
                    <td>Yaoundé → Bafoussam<br><small class="text-muted">280 km</small></td>
                    <td>15/09/2025 - 14:00<br><small class="text-muted">Durée: 5h</small></td>
                    <td><strong>6,500 XAF</strong></td>
                    <td><span class="badge bg-danger">55/55</span></td>
                    <td>CM-5678-CD<br><small class="text-muted">Marie Martin</small></td>
                    <td><span class="badge bg-warning">🟡 En cours</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Modifier">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-success" title="Suivre">
                            <i class="fas fa-route"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    loadTickets() {
        const tbody = document.getElementById('ticketsTable');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td><code>TK-001-2025</code></td>
                    <td><strong>Pierre Martin</strong><br><small class="text-muted">+237 699 123 456</small></td>
                    <td>Douala → Yaoundé</td>
                    <td>15/09/2025 - 08:00</td>
                    <td>CM-1234-AB</td>
                    <td><span class="badge bg-info">Places 12-13</span></td>
                    <td><span class="badge bg-success">Généré</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" title="Imprimer">
                            <i class="fas fa-print"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info" title="Email">
                            <i class="fas fa-envelope"></i>
                        </button>
                    </td>
                </tr>
            `;
        }
    }
}

// Fonctions globales pour la navigation
function showSection(sectionName) {
    // Masquer toutes les sections
    const sections = document.querySelectorAll('.section-content');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    
    // Afficher la section demandée
    const targetSection = document.getElementById(sectionName + '-section');
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Mettre à jour la navigation active
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Activer le lien correspondant
    const activeLink = document.querySelector(`a[onclick="showSection('${sectionName}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
    // Charger les données spécifiques à la section
    if (window.admin) {
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
}
                window.admin.loadBuses();
                break;
            case 'drivers':
                window.admin.loadDrivers();
                break;
            case 'reservations':
                window.admin.loadReservations();
                break;
        }
    }
}

function showCreateTripModal() {
    const modal = new bootstrap.Modal(document.getElementById('createTripModal'));
    modal.show();
}

function showCreateBusModal() {
    const modal = new bootstrap.Modal(document.getElementById('createBusModal'));
    modal.show();
}

function showCreateDriverModal() {
    const modal = new bootstrap.Modal(document.getElementById('createDriverModal'));
    modal.show();
}

function createBus() {
    // Récupérer les données du formulaire
    const form = document.getElementById('createBusForm');
    const formData = new FormData(form);
    
    // Récupérer le statut sélectionné
    const status = formData.get('status');
    
    // Validation simple
    if (!formData.get('registration_number') || !status) {
        alert('⚠️ Veuillez remplir au moins le numéro d\'immatriculation et le statut.');
        return;
    }
    
    // Simulation de l'ajout avec animation
    const submitButton = document.querySelector('[onclick="createBus()"]');
    const originalText = submitButton.innerHTML;
    
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Création en cours...';
    submitButton.disabled = true;
    
    // Simuler un délai pour l'animation
    setTimeout(() => {
        // Afficher un message de succès avec le statut
        const statusEmoji = {
            'disponible': '🟢',
            'en_voyage': '🟡', 
            'en_panne': '🔴',
            'maintenance': '🔧',
            'hors_service': '⚫'
        };
        
        const statusText = {
            'disponible': 'Disponible',
            'en_voyage': 'En voyage',
            'en_panne': 'En panne', 
            'maintenance': 'En maintenance',
            'hors_service': 'Hors service'
        };
        
        alert(`✅ Bus ${formData.get('registration_number')} créé avec succès!\n${statusEmoji[status]} Statut: ${statusText[status]}`);
        
        // Fermer le modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createBusModal'));
        modal.hide();
        
        // Réinitialiser le formulaire
        form.reset();
        
        // Recharger la liste des bus si on est sur cette section
        if (document.getElementById('buses-section').style.display !== 'none') {
            window.admin.loadBuses();
        }
        
        // Restaurer le bouton
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
        
    }, 1500);
}

// Fonction pour afficher le modal de création de chauffeur
function showCreateDriverModal() {
    const modal = new bootstrap.Modal(document.getElementById('createDriverModal'));
    modal.show();
}

// Fonction pour créer un nouveau chauffeur
function createDriver() {
    const form = document.getElementById('createDriverForm');
    const formData = new FormData(form);
    
    // Vérifier les champs obligatoires
    const firstName = formData.get('first_name');
    const lastName = formData.get('last_name');
    const phone = formData.get('phone');
    const idNumber = formData.get('id_number');
    const licenseNumber = formData.get('license_number');
    const licenseCategory = formData.get('license_category');
    const status = formData.get('status');
    
    if (!firstName || !lastName || !phone || !idNumber || !licenseNumber || !licenseCategory || !status) {
        alert('❌ Veuillez remplir tous les champs obligatoires (marqués d\'un *)');
        return;
    }
    
    // Valider le format du téléphone
    const phoneRegex = /^(\+237|237)?[6-9]\d{8}$/;
    if (!phoneRegex.test(phone.replace(/\s/g, ''))) {
        alert('❌ Format de téléphone invalide. Utilisez le format: +237 6XX XXX XXX');
        return;
    }
    
    // Animation du bouton
    const submitButton = document.querySelector('#createDriverModal .btn-primary');
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Création en cours...';
    submitButton.disabled = true;
    
    // Simuler un délai pour l'animation
    setTimeout(() => {
        // Afficher un message de succès avec le statut
        const statusEmoji = {
            'actif': '🟢',
            'en_conge': '🟡', 
            'malade': '🔴',
            'suspendu': '⚫',
            'inactif': '⚪'
        };
        
        const statusText = {
            'actif': 'Actif',
            'en_conge': 'En congé',
            'malade': 'Malade', 
            'suspendu': 'Suspendu',
            'inactif': 'Inactif'
        };
        
        const categoryText = {
            'D': 'Transport en commun',
            'D1': 'Minibus',
            'DE': 'Avec remorque',
            'C': 'Poids lourd'
        };
        
        alert(`✅ Chauffeur ${firstName} ${lastName} créé avec succès!\n🚗 Permis: Catégorie ${licenseCategory} (${categoryText[licenseCategory]})\n${statusEmoji[status]} Statut: ${statusText[status]}`);
        
        // Fermer le modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createDriverModal'));
        modal.hide();
        
        // Réinitialiser le formulaire
        form.reset();
        
        // Recharger la liste des chauffeurs si on est sur cette section
        if (document.getElementById('drivers-section').style.display !== 'none') {
            window.admin.loadDrivers();
        }
        
        // Restaurer le bouton
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
        
    }, 2000);
}

// Fonction pour afficher le modal de création de voyage
function showCreateTripModal() {
    const modal = new bootstrap.Modal(document.getElementById('createTripModal'));
    
    // Définir la date minimum à aujourd'hui
    const today = new Date().toISOString().split('T')[0];
    document.querySelector('#createTripModal input[name="departure_date"]').min = today;
    
    modal.show();
}

// Fonction pour créer un nouveau voyage
function createTrip() {
    const form = document.getElementById('createTripForm');
    const formData = new FormData(form);
    
    // Vérifier les champs obligatoires
    const departureCity = formData.get('departure_city');
    const arrivalCity = formData.get('arrival_city');
    const departureDate = formData.get('departure_date');
    const departureTime = formData.get('departure_time');
    const price = formData.get('price');
    const availableSeats = formData.get('available_seats');
    const bus = formData.get('bus');
    const driver = formData.get('driver');
    
    if (!departureCity || !arrivalCity || !departureDate || !departureTime || !price || !availableSeats || !bus || !driver) {
        alert('❌ Veuillez remplir tous les champs obligatoires (marqués d\'un *)');
        return;
    }
    
    // Vérifier que les villes de départ et d'arrivée sont différentes
    if (departureCity === arrivalCity) {
        alert('❌ La ville de départ et d\'arrivée doivent être différentes');
        return;
    }
    
    // Vérifier que la date n'est pas dans le passé
    const selectedDate = new Date(departureDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (selectedDate < today) {
        alert('❌ La date de départ ne peut pas être dans le passé');
        return;
    }
    
    // Animation du bouton
    const submitButton = document.querySelector('#createTripModal .btn-primary');
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Création en cours...';
    submitButton.disabled = true;
    
    // Simuler un délai pour l'animation
    setTimeout(() => {
        const cityNames = {
            'douala': 'Douala',
            'yaounde': 'Yaoundé',
            'bafoussam': 'Bafoussam',
            'bamenda': 'Bamenda',
            'garoua': 'Garoua',
            'maroua': 'Maroua'
        };
        
        alert(`✅ Voyage créé avec succès!\n🚌 ${cityNames[departureCity]} → ${cityNames[arrivalCity]}\n📅 ${departureDate} à ${departureTime}\n💰 Prix: ${price} XAF\n🪑 ${availableSeats} places disponibles`);
        
        // Fermer le modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createTripModal'));
        modal.hide();
        
        // Réinitialiser le formulaire
        form.reset();
        
        // Recharger la liste des voyages si on est sur cette section
        if (document.getElementById('trips-section').style.display !== 'none') {
            window.admin.loadTrips();
        }
        
        // Restaurer le bouton
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
        
    }, 2000);
}

function logout() {
    localStorage.clear();
    window.location.href = '/auth/login/';
}

// Initialiser l'application
document.addEventListener('DOMContentLoaded', () => {
    window.admin = new AdminBackoffice();
});