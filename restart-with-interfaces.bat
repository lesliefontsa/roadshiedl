@echo off
echo ================================================
echo    REDÉMARRAGE AVEC INTERFACES ACTIVÉES
echo ================================================

cd /d "C:\Users\user\RoadShiel Sentinelle\backend"

echo Arrêt du serveur existant...
taskkill /f /im python.exe 2>nul

echo.
echo Redémarrage du serveur Django...
start "Django Server" python manage.py runserver 8002

echo.
echo  Attente du démarrage du serveur...
timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo           INTERFACES DISPONIBLES
echo ================================================
echo.
echo  Page d'accueil:     http://localhost:8002/
echo  Interface Client:   http://localhost:8002/client/
echo  Dashboard Admin:    http://localhost:8002/admin-dashboard/
echo   Admin Django:      http://localhost:8002/admin/
echo.
echo Comptes de test:
echo   Admin: admin / admin123
echo.
echo Le serveur démarre dans une nouvelle fenêtre...
echo ================================================

echo.
echo Ouvrir automatiquement les interfaces ? (o/n)
set /p choice="Tapez 'o' pour oui: "
if /i "%choice%"=="o" (
    start http://localhost:8002/
    timeout /t 2 /nobreak >nul
    start http://localhost:8002/client/
    timeout /t 2 /nobreak >nul
    start http://localhost:8002/admin-dashboard/
)

pause