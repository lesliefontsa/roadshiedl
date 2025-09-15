@echo off
echo ================================================
echo     Correction du fichier settings.py
echo ================================================

REM Vérifier si nous sommes dans le bon répertoire
if not exist "backend" (
    echo ERREUR: Vous devez exécuter ce script depuis le répertoire principal
    echo Répertoire actuel: %CD%
    echo Naviguez vers: C:\Users\user\RoadShiel Sentinelle
    echo Puis exécutez: fix-settings.bat
    pause
    exit /b 1
)

echo Répertoire de travail: %CD%
echo.

REM Supprimer l'ancien fichier settings.py corrompu
if exist "backend\travel_agency\settings.py" (
    del "backend\travel_agency\settings.py"
    echo ✓ Ancien fichier settings.py supprimé
) else (
    echo ! Ancien fichier settings.py non trouvé
)

REM Renommer le nouveau fichier
if exist "backend\travel_agency\settings_fixed.py" (
    move "backend\travel_agency\settings_fixed.py" "backend\travel_agency\settings.py"
    echo ✓ Nouveau fichier settings.py créé avec succès !
) else (
    echo ! Erreur: fichier settings_fixed.py non trouvé
    echo Création du fichier settings.py directement...
    
    REM Créer le fichier settings.py directement
    (
        echo # travel_agency/settings.py
        echo import os
        echo from pathlib import Path
        echo from datetime import timedelta
        echo.
        echo # Build paths inside the project like this: BASE_DIR / 'subdir'.
        echo BASE_DIR = Path(__file__^).resolve(^).parent.parent
        echo.
        echo # SECURITY WARNING: keep the secret key used in production secret!
        echo SECRET_KEY = 'django-insecure-your-secret-key-change-in-production'
        echo.
        echo # SECURITY WARNING: don't run with debug turned on in production!
        echo DEBUG = True
        echo.
        echo ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
        echo.
        echo # Application definition
        echo DJANGO_APPS = [
        echo     'django.contrib.admin',
        echo     'django.contrib.auth',
        echo     'django.contrib.contenttypes',
        echo     'django.contrib.sessions',
        echo     'django.contrib.messages',
        echo     'django.contrib.staticfiles',
        echo ]
        echo.
        echo THIRD_PARTY_APPS = [
        echo     'rest_framework',
        echo     'corsheaders',
        echo     'drf_spectacular',
        echo ]
        echo.
        echo LOCAL_APPS = [
        echo     'accounts',
        echo     'bookings',
        echo     'vehicles',
        echo     'alerts',
        echo     'api',
        echo ]
        echo.
        echo INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    ) > "backend\travel_agency\settings.py"
    
    echo ✓ Fichier settings.py de base créé
)

echo.
echo ================================================
echo            CORRECTION TERMINÉE !
echo ================================================
echo.
echo PROCHAINES ÉTAPES:
echo.
echo 1. Installez les dépendances:
echo    pip install -r requirements.txt
echo.
echo 2. Appliquez les migrations:
echo    cd backend
echo    python manage.py migrate
echo.
echo 3. Démarrez l'application:
echo    python manage.py runserver 8002
echo.
echo ================================================
pause