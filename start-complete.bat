@echo off
echo ================================================
echo   DÉMARRAGE RAPIDE - RoadShield Travel Agency
echo ================================================

REM Forcer le bon répertoire
cd /d "C:\Users\user\RoadShiel Sentinelle"

echo Répertoire actuel: %CD%
echo.

REM Vérifier la structure
if not exist "backend" (
    echo ❌ ERREUR: Le dossier 'backend' n'existe pas !
    echo Vérifiez que vous êtes dans le bon projet.
    pause
    exit /b 1
)

if not exist "backend\manage.py" (
    echo ❌ ERREUR: Le fichier 'manage.py' n'existe pas !
    echo Création du fichier manage.py...
    goto :create_manage
)

echo ✓ Structure du projet trouvée
echo.

REM Aller dans le dossier backend
cd backend
echo Maintenant dans: %CD%
echo.

echo Étape 1: Installation des dépendances...
pip install django djangorestframework django-cors-headers

echo.
echo Étape 2: Vérification de Django...
python manage.py check

if %errorlevel% equ 0 (
    echo ✓ Django fonctionne !
    
    echo.
    echo Étape 3: Migrations...
    python manage.py migrate
    
    echo.
    echo ✓ Prêt à démarrer !
    echo.
    echo COMMANDES POUR DÉMARRER:
    echo   cd backend
    echo   python manage.py runserver 8002
    echo.
    echo Puis ouvrez: http://localhost:8002/admin
    
) else (
    echo ❌ Erreur dans Django
)

goto :end

:create_manage
echo Création du fichier manage.py...
(
    echo #!/usr/bin/env python
    echo """Django's command-line utility for administrative tasks."""
    echo import os
    echo import sys
    echo.
    echo def main(^):
    echo     """Run administrative tasks."""
    echo     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings'^)
    echo     try:
    echo         from django.core.management import execute_from_command_line
    echo     except ImportError as exc:
    echo         raise ImportError(
    echo             "Couldn't import Django. Are you sure it's installed and "
    echo             "available on your PYTHONPATH environment variable? Did you "
    echo             "forget to activate a virtual environment?"
    echo         ^) from exc
    echo     execute_from_command_line(sys.argv^)
    echo.
    echo if __name__ == '__main__':
    echo     main(^)
) > "backend\manage.py"
echo ✓ Fichier manage.py créé
cd backend

:end
echo.
echo ================================================
pause