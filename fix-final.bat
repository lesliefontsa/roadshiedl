@echo off
echo ================================================
echo   CORRECTION FINALE du fichier settings.py
echo ================================================

REM Aller dans le bon répertoire
cd /d "C:\Users\user\RoadShiel Sentinelle"

echo Suppression de l'ancien fichier corrompu...
if exist "backend\travel_agency\settings.py" (
    del "backend\travel_agency\settings.py"
    echo ✓ Ancien fichier supprimé
)

echo Copie du nouveau fichier propre...
if exist "backend\travel_agency\settings_clean.py" (
    copy "backend\travel_agency\settings_clean.py" "backend\travel_agency\settings.py"
    echo ✓ Nouveau fichier settings.py créé !
) else (
    echo ! Fichier settings_clean.py non trouvé, création manuelle...
    goto :create_manual
)

goto :success

:create_manual
echo Création manuelle du fichier settings.py...
mkdir "backend\travel_agency" 2>nul

echo # travel_agency/settings.py > "backend\travel_agency\settings.py"
echo import os >> "backend\travel_agency\settings.py"
echo from pathlib import Path >> "backend\travel_agency\settings.py"
echo from datetime import timedelta >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo BASE_DIR = Path(__file__^).resolve(^).parent.parent >> "backend\travel_agency\settings.py"
echo SECRET_KEY = 'django-insecure-roadshield-key-2024' >> "backend\travel_agency\settings.py"
echo DEBUG = True >> "backend\travel_agency\settings.py"
echo ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*'] >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo INSTALLED_APPS = [ >> "backend\travel_agency\settings.py"
echo     'django.contrib.admin', >> "backend\travel_agency\settings.py"
echo     'django.contrib.auth', >> "backend\travel_agency\settings.py"
echo     'django.contrib.contenttypes', >> "backend\travel_agency\settings.py"
echo     'django.contrib.sessions', >> "backend\travel_agency\settings.py"
echo     'django.contrib.messages', >> "backend\travel_agency\settings.py"
echo     'django.contrib.staticfiles', >> "backend\travel_agency\settings.py"
echo     'rest_framework', >> "backend\travel_agency\settings.py"
echo     'corsheaders', >> "backend\travel_agency\settings.py"
echo ] >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo MIDDLEWARE = [ >> "backend\travel_agency\settings.py"
echo     'corsheaders.middleware.CorsMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.middleware.security.SecurityMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.contrib.sessions.middleware.SessionMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.middleware.common.CommonMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.middleware.csrf.CsrfViewMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.contrib.auth.middleware.AuthenticationMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.contrib.messages.middleware.MessageMiddleware', >> "backend\travel_agency\settings.py"
echo     'django.middleware.clickjacking.XFrameOptionsMiddleware', >> "backend\travel_agency\settings.py"
echo ] >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo ROOT_URLCONF = 'travel_agency.urls' >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo DATABASES = { >> "backend\travel_agency\settings.py"
echo     'default': { >> "backend\travel_agency\settings.py"
echo         'ENGINE': 'django.db.backends.sqlite3', >> "backend\travel_agency\settings.py"
echo         'NAME': BASE_DIR / 'db.sqlite3', >> "backend\travel_agency\settings.py"
echo     } >> "backend\travel_agency\settings.py"
echo } >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo LANGUAGE_CODE = 'fr-fr' >> "backend\travel_agency\settings.py"
echo TIME_ZONE = 'UTC' >> "backend\travel_agency\settings.py"
echo USE_I18N = True >> "backend\travel_agency\settings.py"
echo USE_TZ = True >> "backend\travel_agency\settings.py"
echo. >> "backend\travel_agency\settings.py"
echo STATIC_URL = '/static/' >> "backend\travel_agency\settings.py"
echo DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' >> "backend\travel_agency\settings.py"

echo ✓ Fichier settings.py créé manuellement !

:success
echo.
echo ================================================
echo            CORRECTION RÉUSSIE !
echo ================================================
echo.
echo TESTEZ MAINTENANT:
echo.
echo cd backend
echo python manage.py check
echo.
echo Si aucune erreur, continuez avec:
echo python manage.py migrate
echo python manage.py runserver 8002
echo.
echo ================================================
pause