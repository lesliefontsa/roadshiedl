@echo off
echo ===========================================
echo    ROADSHIELD SENTINELLE - LANCEMENT
echo ===========================================

@echo off
echo ===========================================
echo    ROADSHIELD SENTINELLE - LANCEMENT
echo ===========================================

:: Tuer tous les processus Python existants
echo [1/4] Arret des serveurs existants...
taskkill /f /im python.exe >nul 2>&1

:: Aller dans le dossier backend
echo [2/4] Navigation vers backend...
cd /d "%~dp0backend"

:: Verifier que les migrations sont appliquees
echo [3/4] Verification base de donnees...
python manage.py migrate >nul 2>&1

:: Lancer le serveur sur le port 8002
echo [4/4] Demarrage serveur Django sur port 8002...
echo.
echo ✅ SERVEUR DEMARRE !
echo ✅ Interface Admin: http://localhost:8002/admin-backoffice/
echo ✅ Interface Client: http://localhost:8002/
echo.
echo Comptes de test:
echo - Admin: admin / admin123
echo - Client: client / client123
echo.
echo CTRL+C pour arreter
echo.
python manage.py runserver 8002
echo ===========================================
python manage.py runserver 8002