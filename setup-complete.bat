@echo off
echo ================================================
echo    ACTIVATION COMPLÈTE - Toutes Fonctionnalités
echo ================================================

cd /d "C:\Users\user\RoadShiel Sentinelle\backend"

echo Étape 1: Suppression base de données pour rebuild complet...
if exist "db.sqlite3" del "db.sqlite3"

echo.
echo Étape 2: Installation dépendances paiement...
pip install stripe python-dotenv requests

echo.
echo Étape 3: Création des migrations pour toutes les apps...
python manage.py makemigrations accounts --empty
python manage.py makemigrations bookings --empty  
python manage.py makemigrations vehicles --empty
python manage.py makemigrations alerts --empty

echo.
echo Étape 4: Application des migrations Django de base...
python manage.py migrate

echo.
echo Étape 5: Création superutilisateur et données test...
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@roadshield.com', 'admin123')
    print('✓ Superutilisateur créé: admin/admin123')
"

echo.
echo ✓ Configuration terminée !
echo.
echo Démarrage du serveur...
python manage.py runserver 8002