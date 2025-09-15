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
                    <td><strong>Jean Dupont</strong></td>
                    <td>+237 699 123 456</td>
                    <td>CM-PERM-2023</td>
                    <td><span class="badge bg-success">CM-1234-AB</span></td>
                    <td>⭐⭐⭐⭐☆ 4.0</td>
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
}

// Fonctions globales simplifiées
function showSection(sectionName) {
    // Cacher toutes les sections
    document.querySelectorAll('.section-content').forEach(section => {
        section.style.display = 'none';
    });
    
    // Afficher la section demandée
    const targetSection = document.getElementById(sectionName + '-section');
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Charger les données selon la section
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

function logout() {
    localStorage.clear();
    window.location.href = '/auth/login/';
}

// Initialiser l'application
document.addEventListener('DOMContentLoaded', () => {
    window.admin = new AdminBackoffice();
});