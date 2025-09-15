@echo off
echo ================================================
echo   ROADSHIELD TRAVEL - Orange Money Integration
echo ================================================

cd /d "C:\Users\user\RoadShiel Sentinelle\backend"

echo 🍊 Démarrage avec intégration Orange Money...
echo.
echo INTERFACES DISPONIBLES:
echo   🏠 http://localhost:8002/               (Accueil)
echo   🛒 http://localhost:8002/client/        (Interface Client avec Orange Money)
echo   📊 http://localhost:8002/admin-dashboard/ (Dashboard Admin)
echo   📈 http://localhost:8002/reports/       (Rapports Orange Money)
echo   ⚙️  http://localhost:8002/admin/         (Admin Django)
echo.
echo APIS ORANGE MONEY:
echo   💳 /api/payment/process/               (Paiement principal)
echo   🍊 /api/payment/orange/init/           (Initialisation Orange Money)
echo   📱 /api/payment/orange/simulate/       (Simulation paiement)
echo   📊 /api/payment/reports/               (Rapports détaillés)
echo   💰 /api/payment/orange/balance/        (Solde Orange Money)
echo.
echo Comptes de test: admin / admin123
echo Numéros Orange Money test: +237 6XX XXX XXX
echo.
echo ================================================
echo Le serveur Orange Money va démarrer...
echo ================================================
echo.

python manage.py runserver 8002