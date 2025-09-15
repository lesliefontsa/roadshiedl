# Documentation de l'Application RoadShield Travel Agency

## Vue d'ensemble

RoadShield Travel Agency est une application complète de gestion de voyage pour les agences routières qui intègre :

- **Backend Django + FastAPI** : API REST et endpoints pour Arduino
- **Frontend Bootstrap + JavaScript** : Interface client et admin modernes
- **Système d'alertes** : Surveillance en temps réel des chauffeurs
- **Authentification JWT** : Système sécurisé pour clients et admin
- **Integration Arduino** : Réception de données de capteurs IoT

## Architecture du Projet

```
RoadShiel Sentinelle/
├── backend/
│   ├── travel_agency/          # Configuration Django principale
│   ├── accounts/               # Gestion des utilisateurs
│   ├── bookings/              # Système de réservations
│   ├── vehicles/              # Gestion des véhicules
│   ├── alerts/                # Système d'alertes
│   ├── api/                   # API FastAPI pour Arduino
│   └── manage.py
├── frontend/
│   ├── index.html             # Dashboard admin
│   ├── client.html            # Interface client
│   ├── client-app.js          # Application JavaScript client
│   └── style.css              # Styles CSS
├── arduino_example.ino        # Code exemple Arduino
├── requirements.txt           # Dépendances Python
├── start.sh / start.bat       # Scripts de démarrage
└── README.md
```

## Fonctionnalités Principales

### Côté Client
- **Recherche de voyages** : Par ville, date, nombre de passagers
- **Réservation en ligne** : Interface intuitive avec paiement
- **Gestion de compte** : Inscription, connexion, profil
- **Suivi des réservations** : Historique et statut des voyages

### Côté Admin
- **Dashboard en temps réel** : Surveillance des véhicules et chauffeurs
- **Gestion des alertes** : Somnolence, fatigue, excès de vitesse
- **Suivi GPS** : Position et vitesse des véhicules
- **Gestion des réservations** : Validation et suivi des bookings

### Intégration Arduino
- **Capteurs biométriques** : Détection de somnolence et fatigue
- **Données de conduite** : Vitesse, freinage, accélération
- **Géolocalisation** : Position GPS en temps réel
- **Alertes automatiques** : Notification immédiate des incidents

## Installation et Configuration

### Prérequis
- Python 3.8+
- PostgreSQL installé et configuré
- Git pour cloner le projet

### Installation Rapide
1. **Naviguer vers le répertoire backend** :
   ```powershell
   cd "C:\Users\user\RoadShiel Sentinelle\backend"
   ```

2. **Installer les dépendances** :
   ```bash
   pip install django psycopg2-binary
   ```

3. **Configurer et lancer l'application** :
   ```powershell
   # Option 1: Script automatique (recommandé)
   ..\launch.ps1
   
   # Option 2: Manuel
   python setup_database.py
   python manage.py runserver 8002
   ```

### Structure des Répertoires
```
RoadShiel Sentinelle/
├── backend/                    # ⚠️ RÉPERTOIRE PRINCIPAL
│   ├── manage.py              # ✅ Fichier de gestion Django
│   ├── setup_database.py      # ✅ Configuration automatique
│   ├── travel_agency/         # Configuration Django
│   ├── travel/                # App principale
│   ├── vehicles/              # Gestion véhicules
│   ├── alerts/                # Système d'alertes
│   └── accounts/              # Comptes utilisateurs
├── launch.ps1                 # Script de lancement automatique
└── README.md
```

### Démarrage des Serveurs
1. **Django** (API principal) :
   ```bash
   cd backend
   python manage.py runserver 8002
   ```

2. **FastAPI** (Arduino API) :
   ```bash
   cd backend
   python api/fastapi_app.py
   ```

### URLs d'Accès
- **Interface Client** : http://localhost:8002/client.html
- **Dashboard Admin** : http://localhost:8002/index.html
- **API Documentation** : http://localhost:8003/docs
- **Admin Django** : http://localhost:8002/admin

## Comptes de Test

- **Admin** : admin / admin123
- **Chauffeurs** : emmanuel / driver123, ayina / driver123, syntyche / driver123

## API Endpoints

### Authentification
- `POST /api/auth/login/` - Connexion utilisateur
- `POST /api/auth/register/` - Inscription utilisateur
- `GET /api/auth/profile/` - Profil utilisateur

### Réservations
- `GET /api/bookings/routes/` - Liste des routes
- `GET /api/bookings/trips/search/` - Recherche de voyages
- `POST /api/bookings/booking/create/` - Créer une réservation

### Alertes
- `GET /api/alerts/` - Liste des alertes
- `POST /api/alerts/{id}/acknowledge/` - Accusé réception alerte
- `GET /api/alerts/dashboard-stats/` - Statistiques dashboard

### Arduino (FastAPI)
- `POST /arduino/data` - Recevoir données capteurs
- `GET /arduino/vehicle/{device_id}/status` - Statut véhicule
- `GET /arduino/alerts/recent` - Alertes récentes

## Configuration Arduino

### Matériel Nécessaire
- ESP32 ou Arduino avec WiFi
- Capteur de mouvement oculaire
- Accéléromètre/Gyroscope
- Module GPS
- Capteurs de vitesse et freinage

### Configuration WiFi
Modifier dans `arduino_example.ino` :
```cpp
const char* ssid = "VotreWiFi";
const char* password = "VotreMotDePasse";
const char* api_url = "http://votre-serveur:8001/arduino/data";
```

## Fonctionnalités Avancées

### Détection de Somnolence
- Analyse de la fermeture des yeux
- Détection de mouvements de tête
- Calcul du niveau de fatigue (1-10)
- Alertes automatiques selon la criticité

### Surveillance de Conduite
- Détection d'excès de vitesse
- Freinage et accélération brusques
- Déviation de route
- Score de conduite global

### Gestion des Alertes
- Classification par sévérité (faible, modéré, élevé, critique)
- Workflow d'accusé réception et résolution
- Notifications en temps réel
- Historique complet

## Sécurité

### Authentification
- JWT avec expiration automatique
- Rôles utilisateurs (admin, agent, client, driver)
- Permissions granulaires par endpoint

### Protection des Données
- Validation des entrées
- Protection CSRF
- CORS configuré
- Données sensibles chiffrées

## Déploiement en Production

### Variables d'Environnement
Configurer dans `.env` :
```
DEBUG=False
SECRET_KEY=votre-clé-secrète-production
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=votre-domaine.com
```

### Base de Données
Passer de SQLite à PostgreSQL pour la production :
```python
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

## Support et Maintenance

### Logs et Monitoring
- Logs Django pour le debugging
- Monitoring des performances API
- Alertes système automatiques
- Sauvegarde régulière des données

### Extensions Possibles
- Intégration cartes (OpenStreetMap, Google Maps)
- Notifications push mobiles
- Analyse prédictive de fatigue
- Interface mobile native
- Intégration systèmes de paiement

## Contact et Support

Pour toute question ou assistance, consultez la documentation API à l'adresse :
http://localhost:8001/docs (FastAPI)
http://localhost:8000/api/docs/ (Django)

---

*Cette application a été conçue pour assurer la sécurité maximale des voyageurs grâce à une surveillance avancée des chauffeurs et une gestion moderne des réservations.*