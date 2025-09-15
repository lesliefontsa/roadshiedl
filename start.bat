@echo off
REM Script de démarrage pour Windows

echo === Démarrage de RoadShield Travel Agency ===

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements.txt

REM Changer vers le répertoire backend
cd backend

REM Effectuer les migrations
echo Application des migrations...
python manage.py makemigrations
python manage.py migrate

REM Créer un superutilisateur
echo Création du superutilisateur...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')"

echo === Application prête ===
echo.
echo Pour démarrer:
echo 1. Django: python manage.py runserver 8002
echo 2. FastAPI: python api/fastapi_app.py
echo 3. Ouvrir: http://localhost:8002/client.html
echo.
pause