# Fichier de démarrage rapide avec gestion des ports
@echo off
echo ==============================================
echo     RoadShield Travel Agency - Démarrage
echo ==============================================
echo.

REM Vérifier si les ports sont disponibles
echo Vérification des ports disponibles...

REM Vérifier le port 8002 (Django)
netstat -an | find "8002" > nul
if %errorlevel% == 0 (
    echo ATTENTION: Le port 8002 est déjà utilisé !
    echo Voulez-vous utiliser un autre port pour Django ? ^(8004^)
    set /p choice="Tapez 'o' pour oui, 'n' pour arrêter: "
    if /i "%choice%"=="o" (
        set DJANGO_PORT=8004
        echo Django utilisera le port 8004
    ) else (
        echo Arrêt du démarrage.
        pause
        exit /b 1
    )
) else (
    set DJANGO_PORT=8002
    echo Port 8002 disponible pour Django
)

REM Vérifier le port 8003 (FastAPI)
netstat -an | find "8003" > nul
if %errorlevel% == 0 (
    echo ATTENTION: Le port 8003 est déjà utilisé !
    echo Voulez-vous utiliser un autre port pour FastAPI ? ^(8005^)
    set /p choice="Tapez 'o' pour oui, 'n' pour arrêter: "
    if /i "%choice%"=="o" (
        set FASTAPI_PORT=8005
        echo FastAPI utilisera le port 8005
    ) else (
        echo Arrêt du démarrage.
        pause
        exit /b 1
    )
) else (
    set FASTAPI_PORT=8003
    echo Port 8003 disponible pour FastAPI
)

echo.
echo Configuration des ports:
echo - Django: %DJANGO_PORT%
echo - FastAPI: %FASTAPI_PORT%
echo.

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

echo.
echo ==============================================
echo            APPLICATION PRÊTE !
echo ==============================================
echo.
echo ÉTAPES SUIVANTES:
echo.
echo 1. Ouvrir un PREMIER terminal et exécuter:
echo    cd backend
echo    python manage.py runserver %DJANGO_PORT%
echo.
echo 2. Ouvrir un DEUXIÈME terminal et exécuter:
echo    cd backend  
echo    python api/fastapi_app.py
echo.
echo 3. Ouvrir votre navigateur:
echo    - Interface Client: http://localhost:%DJANGO_PORT%/client.html
echo    - Dashboard Admin: http://localhost:%DJANGO_PORT%/index.html
echo    - API Documentation: http://localhost:%FASTAPI_PORT%/docs
echo.
echo COMPTES DE TEST:
echo - Admin: admin / admin123
echo - Chauffeur: emmanuel / driver123
echo.
echo ==============================================
pause