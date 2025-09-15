@echo off
echo ================================================
echo     DÉMARRAGE DJANGO - Solution Complète
echo ================================================

REM Forcer le bon répertoire
cd /d "C:\Users\user\RoadShiel Sentinelle"
echo Répertoire principal: %CD%

REM Vérifier que backend existe
if not exist "backend" (
    echo ❌ ERREUR: Le dossier backend n'existe pas !
    echo Création du dossier backend...
    mkdir backend
)

REM Aller dans backend
cd backend
echo Maintenant dans: %CD%

REM Vérifier si manage.py existe
if not exist "manage.py" (
    echo ❌ manage.py manquant, création...
    echo #!/usr/bin/env python > manage.py
    echo """Django's command-line utility for administrative tasks.""" >> manage.py
    echo import os >> manage.py
    echo import sys >> manage.py
    echo. >> manage.py
    echo def main(): >> manage.py
    echo     """Run administrative tasks.""" >> manage.py
    echo     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings'^) >> manage.py
    echo     try: >> manage.py
    echo         from django.core.management import execute_from_command_line >> manage.py
    echo     except ImportError as exc: >> manage.py
    echo         raise ImportError( >> manage.py
    echo             "Couldn't import Django." >> manage.py
    echo         ^) from exc >> manage.py
    echo     execute_from_command_line(sys.argv^) >> manage.py
    echo. >> manage.py
    echo if __name__ == '__main__': >> manage.py
    echo     main(^) >> manage.py
    echo ✓ manage.py créé
)

echo.
echo Étape 1: Installation des dépendances...
pip install django djangorestframework django-cors-headers

echo.
echo Étape 2: Test de Django...
python manage.py check

if %errorlevel% equ 0 (
    echo ✓ Django fonctionne parfaitement !
    
    echo.
    echo Étape 3: Création de la base de données...
    python manage.py migrate
    
    echo.
    echo ✓ Installation terminée avec succès !
    echo.
    echo ================================================
    echo              PRÊT À UTILISER !
    echo ================================================
    echo.
    echo POUR DÉMARRER LE SERVEUR:
    echo   python manage.py runserver 8002
    echo.
    echo PUIS OUVREZ DANS LE NAVIGATEUR:
    echo   http://localhost:8002/
    echo   http://localhost:8002/admin/
    echo.
    echo ================================================
    
) else (
    echo ❌ Erreur détectée dans Django
    echo Vérifiez les messages d'erreur ci-dessus
)

pause