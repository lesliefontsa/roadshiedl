@echo off
echo ================================================
echo   Installation et Test Django Minimal
echo ================================================

cd /d "C:\Users\user\RoadShiel Sentinelle"

echo Étape 1: Installation des dépendances de base...
pip install django djangorestframework django-cors-headers

echo.
echo Étape 2: Test de Django...
cd backend
python manage.py check

if %errorlevel% equ 0 (
    echo ✓ Django fonctionne !
    echo.
    echo Étape 3: Création de la base de données...
    python manage.py migrate
    
    echo.
    echo Étape 4: Création d'un superutilisateur...
    echo Créez votre compte admin:
    python manage.py createsuperuser
    
    echo.
    echo ✓ Installation terminée !
    echo.
    echo POUR DÉMARRER L'APPLICATION:
    echo python manage.py runserver 8002
    echo.
    echo Puis ouvrez: http://localhost:8002/admin
    
) else (
    echo ❌ Erreur dans Django, vérifiez les messages ci-dessus
)

echo.
echo ================================================
pause