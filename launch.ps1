# Launch RoadShield Travel Agency
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "      LANCEMENT - RoadShield Travel Agency" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Aller dans le bon répertoire
Set-Location "C:\Users\user\RoadShiel Sentinelle\backend"

Write-Host "🔧 Configuration de la base de données PostgreSQL..." -ForegroundColor Yellow
python setup_database.py

Write-Host ""
Write-Host "🚀 Démarrage du serveur Django..." -ForegroundColor Green
Write-Host ""
Write-Host "INTERFACES DISPONIBLES:" -ForegroundColor Yellow
Write-Host "   🔐 http://localhost:8002/auth/login/      (Page de Connexion)" -ForegroundColor White
Write-Host "   �‍💼 http://localhost:8002/admin-dashboard/   (Dashboard Admin)" -ForegroundColor White  
Write-Host "   � http://localhost:8002/client-dashboard/  (Dashboard Client)" -ForegroundColor White
Write-Host "   ⚙️  http://localhost:8002/admin/            (Admin Django)" -ForegroundColor White
Write-Host ""
Write-Host "COMPTES DISPONIBLES:" -ForegroundColor Cyan
Write-Host "   👨‍💼 admin / admin123    (Administrateur Principal)" -ForegroundColor White
Write-Host "   👨‍💼 manager / manager123 (Manager Transport)" -ForegroundColor White
Write-Host "   👤 client1 / client123  (Client Jean Dupont)" -ForegroundColor White
Write-Host "   👤 marie / marie123     (Client Marie Ngono)" -ForegroundColor White
Write-Host "   👤 paul / paul123       (Client Paul Mbassa)" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🔒 AUTHENTIFICATION OBLIGATOIRE POUR TOUTES LES PAGES" -ForegroundColor Red
Write-Host "Le serveur va démarrer..." -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Red
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Démarrer Django
python manage.py runserver 8002