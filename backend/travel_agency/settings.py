# travel_agency/settings.py
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-roadshield-travel-agency-2024'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'travel', 
    'vehicles',
    'alerts',  # Réactivé pour les alertes
    'api',
    # 'bookings',  # Désactivé temporairement pour éviter conflits
    # 'accounts',  # Désactivé pour éviter complications
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'travel_agency.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'travel_agency' / 'templates',  # Templates du projet principal
            BASE_DIR / 'travel' / 'templates',         # Templates de l'app travel
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'travel_agency.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuration PostgreSQL (pour plus tard)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'roadshield_travel',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR.parent,  # Pour servir les fichiers du répertoire parent (client.html, etc.)
    BASE_DIR / 'travel_agency' / 'static',  # Pour les fichiers statiques du backoffice
]

# Media files (User uploads, PDFs, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Orange Money API Configuration (Simulation)
ORANGE_MONEY_CONFIG = {
    'BASE_URL': 'https://api.orange.com/orange-money-webpay/cm/v1',
    'CLIENT_ID': 'your-orange-client-id',
    'CLIENT_SECRET': 'your-orange-client-secret',
    'MERCHANT_KEY': 'your-merchant-key',
    'RETURN_URL': 'http://localhost:8002/api/payment/orange/callback/',
    'CANCEL_URL': 'http://localhost:8002/api/payment/orange/cancel/',
    'NOTIF_URL': 'http://localhost:8002/api/payment/orange/notification/',
}

# Simulation mode pour Orange Money
ORANGE_MONEY_SIMULATION = True

# Configuration du modèle utilisateur personnalisé
AUTH_USER_MODEL = 'travel.CustomUser'

# Configuration pour rediriger vers login
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'

# Configuration CORS pour permettre les requêtes frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8009",
    "http://127.0.0.1:8009",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

# Trusted origins pour CSRF
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8009',
    'http://127.0.0.1:8009',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Configuration Stripe (clés de test - à configurer dans .env)
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'your_stripe_public_key_here')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'your_stripe_secret_key_here')