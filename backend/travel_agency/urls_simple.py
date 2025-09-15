from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
import os

def home_view(request):
    """Page de login directe - première page de l'application"""
    # Si l'utilisateur est déjà connecté, rediriger selon son rôle
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'role') and user.role == 'admin':
            return redirect('/admin-backoffice/')
        else:
            return redirect('/client-fixed.html')
    
    # Traitement de la connexion
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentification simple avec comptes de test
        test_accounts = {
            'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Administrateur Principal'},
            'manager': {'password': 'manager123', 'role': 'admin', 'name': 'Manager Transport'},
            'client1': {'password': 'client123', 'role': 'client', 'name': 'Jean Dupont'},
            'marie': {'password': 'marie123', 'role': 'client', 'name': 'Marie Ngono'},
            'paul': {'password': 'paul123', 'role': 'client', 'name': 'Paul Mbassa'},
        }
        
        if username in test_accounts and test_accounts[username]['password'] == password:
            # Connexion réussie - stocker les informations utilisateur
            user_info = {
                'username': username,
                'role': test_accounts[username]['role'],
                'first_name': test_accounts[username]['name'].split()[0],
                'last_name': ' '.join(test_accounts[username]['name'].split()[1:]),
                'full_name': test_accounts[username]['name']
            }
            
            # Redirection selon le rôle
            if user_info['role'] == 'admin':
                redirect_url = '/admin-backoffice/'
            else:
                redirect_url = '/client-fixed.html'
            
            return HttpResponse(f"""
                <script>
                    localStorage.setItem('authToken', 'token_{username}');
                    localStorage.setItem('userInfo', '{json.dumps(user_info)}');
                    window.location.href = '{redirect_url}';
                </script>
            """)
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
    else:
        error_message = ""
    
    # Afficher la page de login
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RoadShield Travel - Connexion</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .login-container {{
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(20px);
                border-radius: 25px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.1);
                overflow: hidden;
                max-width: 450px;
                width: 100%;
                animation: slideInUp 0.8s ease-out;
            }}
            
            @keyframes slideInUp {{
                from {{ opacity: 0; transform: translateY(50px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .login-header {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-align: center;
                padding: 40px 20px;
            }}
            
            .logo-icon {{
                font-size: 3rem;
                margin-bottom: 15px;
                animation: bounce 2s ease-in-out infinite;
            }}
            
            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-10px); }}
                60% {{ transform: translateY(-5px); }}
            }}
            
            .login-form {{ padding: 40px 30px; }}
            .form-floating {{ margin-bottom: 20px; }}
            
            .form-control {{
                border-radius: 15px;
                border: 2px solid rgba(102, 126, 234, 0.2);
                padding: 15px 20px;
                transition: all 0.3s ease;
            }}
            
            .form-control:focus {{
                border-color: #667eea;
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
                transform: scale(1.02);
            }}
            
            .btn-login {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                border-radius: 25px;
                padding: 15px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
            }}
            
            .btn-login:hover {{
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
            }}
            
            .test-accounts {{
                background: rgba(102, 126, 234, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
            }}
            
            .test-btn {{
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 10px;
                color: #667eea;
                font-weight: 500;
                margin: 5px;
            }}
            
            .test-btn:hover {{
                background: rgba(102, 126, 234, 0.2);
                transform: scale(1.05);
            }}
            
            .alert {{
                border-radius: 15px;
                border: none;
                animation: shake 0.5s ease-in-out;
            }}
            
            @keyframes shake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-5px); }}
                75% {{ transform: translateX(5px); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="login-container">
                        <div class="login-header">
                            <i class="fas fa-shield-alt logo-icon"></i>
                            <h2>RoadShield Travel</h2>
                            <p class="mb-0">🚀 Connexion Directe</p>
                        </div>
                        
                        <div class="login-form">
                            {error_message and f'<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> {error_message}</div>' or ''}
                            
                            <form method="post">
                                <div class="form-floating">
                                    <input type="text" class="form-control" id="username" name="username" 
                                           placeholder="Nom d'utilisateur" required>
                                    <label for="username">
                                        <i class="fas fa-user"></i> Nom d'utilisateur
                                    </label>
                                </div>
                                
                                <div class="form-floating">
                                    <input type="password" class="form-control" id="password" name="password" 
                                           placeholder="Mot de passe" required>
                                    <label for="password">
                                        <i class="fas fa-lock"></i> Mot de passe
                                    </label>
                                </div>
                                
                                <button type="submit" class="btn btn-login btn-primary w-100">
                                    <i class="fas fa-sign-in-alt"></i> Se Connecter
                                </button>
                            </form>
                            
                            <div class="test-accounts">
                                <h6 class="text-center mb-3">
                                    <i class="fas fa-vial"></i> Comptes de Test
                                </h6>
                                <div class="row">
                                    <div class="col-6">
                                        <small class="fw-bold">Admin:</small><br>
                                        <button class="btn test-btn btn-sm w-100" onclick="fillLogin('admin','admin123')">
                                            admin / admin123
                                        </button>
                                        <button class="btn test-btn btn-sm w-100 mt-1" onclick="fillLogin('manager','manager123')">
                                            manager / manager123
                                        </button>
                                    </div>
                                    <div class="col-6">
                                        <small class="fw-bold">Client:</small><br>
                                        <button class="btn test-btn btn-sm w-100" onclick="fillLogin('client1','client123')">
                                            client1 / client123
                                        </button>
                                        <button class="btn test-btn btn-sm w-100 mt-1" onclick="fillLogin('marie','marie123')">
                                            marie / marie123
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function fillLogin(username, password) {{
                document.getElementById('username').value = username;
                document.getElementById('password').value = password;
                
                const inputs = document.querySelectorAll('.form-control');
                inputs.forEach(input => {{
                    input.style.background = 'rgba(102, 126, 234, 0.1)';
                    setTimeout(() => input.style.background = '', 1000);
                }});
            }}
        </script>
    </body>
    </html>
    """, content_type='text/html')

def serve_login(request):
    """Page de connexion"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Connexion - RoadShield</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                display: flex; 
                align-items: center; 
            }
            .login-card { 
                background: white; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="login-card p-4">
                        <div class="text-center mb-4">
                            <h3><i class="fas fa-shield-alt text-primary"></i> RoadShield Travel</h3>
                            <p class="text-muted">Connexion Sécurisée</p>
                        </div>
                        
                        <div id="alertContainer"></div>
                        
                        <form id="loginForm">
                            <div class="mb-3">
                                <label class="form-label">Nom d'utilisateur</label>
                                <input type="text" class="form-control" id="username" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Mot de passe</label>
                                <input type="password" class="form-control" id="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="fas fa-sign-in-alt"></i> Se Connecter
                            </button>
                        </form>
                        
                        <div class="text-center mt-3">
                            <a href="/register/">Créer un compte</a> | 
                            <a href="/">Retour accueil</a>
                        </div>
                        
                        <div class="mt-4 p-3 bg-light rounded">
                            <h6>Comptes de test :</h6>
                            <div class="row">
                                <div class="col-6">
                                    <strong>Administrateurs :</strong><br>
                                    <button class="btn btn-link btn-sm p-0" onclick="quickLogin('admin','admin123')">admin/admin123</button><br>
                                    <button class="btn btn-link btn-sm p-0" onclick="quickLogin('manager','manager123')">manager/manager123</button>
                                </div>
                                <div class="col-6">
                                    <strong>Clients :</strong><br>
                                    <button class="btn btn-link btn-sm p-0" onclick="quickLogin('client1','client123')">client1/client123</button><br>
                                    <button class="btn btn-link btn-sm p-0" onclick="quickLogin('marie','marie123')">marie/marie123</button><br>
                                    <button class="btn btn-link btn-sm p-0" onclick="quickLogin('paul','paul123')">paul/paul123</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                // Afficher un indicateur de chargement
                const submitBtn = e.target.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connexion...';
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/auth/login/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username, password })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        // Stocker les informations de connexion
                        localStorage.setItem('authToken', data.token);
                        localStorage.setItem('userInfo', JSON.stringify(data.user));
                        
                        showAlert('Connexion réussie ! Redirection...', 'success');
                        
                        // Rediriger selon le rôle
                        setTimeout(() => {
                            if (data.user.role === 'admin') {
                                window.location.href = '/admin-backoffice/';
                            } else {
                                window.location.href = '/client/';
                            }
                        }, 1500);
                        
                    } else {
                        showAlert(data.message || 'Erreur de connexion', 'danger');
                    }
                    
                } catch (error) {
                    console.error('Erreur:', error);
                    showAlert('Erreur de connexion au serveur', 'danger');
                } finally {
                    // Restaurer le bouton
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            });
            
            function showAlert(message, type) {
                const alertHtml = `
                    <div class="alert alert-\${type} alert-dismissible fade show">
                        \${message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                `;
                document.getElementById('alertContainer').innerHTML = alertHtml;
            }
            
            function quickLogin(username, password) {
                document.getElementById('username').value = username;
                document.getElementById('password').value = password;
                document.getElementById('loginForm').dispatchEvent(new Event('submit'));
            }
        </script>
    </body>
    </html>
    """, content_type='text/html')

def serve_register(request):
    """Page d'inscription"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Inscription - RoadShield</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-success">
        <div class="container d-flex justify-content-center align-items-center min-vh-100">
            <div class="card shadow" style="width: 500px;">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Créer un Compte</h3>
                    <form>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <input type="text" class="form-control" placeholder="Prénom">
                            </div>
                            <div class="col-md-6 mb-3">
                                <input type="text" class="form-control" placeholder="Nom">
                            </div>
                        </div>
                        <div class="mb-3">
                            <input type="email" class="form-control" placeholder="Email">
                        </div>
                        <div class="mb-3">
                            <input type="tel" class="form-control" placeholder="Téléphone Orange Money">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" placeholder="Nom d'utilisateur">
                        </div>
                        <div class="mb-3">
                            <input type="password" class="form-control" placeholder="Mot de passe">
                        </div>
                        <button type="submit" class="btn btn-success w-100">Créer le Compte</button>
                    </form>
                    <div class="text-center mt-3">
                        <a href="/login/">Déjà un compte ?</a> | 
                        <a href="/">Retour accueil</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """, content_type='text/html')

def serve_client(request):
    """Interface client complète pour voir et réserver les voyages créés par l'admin"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>RoadShield Travel - Réservation Client</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            /* Navbar avec effet glassmorphism */
            .navbar { 
                background: rgba(255,255,255,0.95) !important; 
                backdrop-filter: blur(20px); 
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }
            
            /* Cards avec animations et effets */
            .card { 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border: none;
                overflow: hidden;
                position: relative;
            }
            
            .card:hover { 
                transform: translateY(-10px); 
                box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            }
            
            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
                background-size: 200% 100%;
                animation: shimmer 3s ease-in-out infinite;
            }
            
            @keyframes shimmer {
                0%, 100% { background-position: 200% 0; }
                50% { background-position: -200% 0; }
            }
            
            /* Voyage cards avec effets premium */
            .voyage-card { 
                border-left: 4px solid transparent;
                background: linear-gradient(white, white) padding-box,
                           linear-gradient(135deg, #28a745, #20c997) border-box;
                margin-bottom: 20px;
                position: relative;
                overflow: hidden;
            }
            
            .voyage-card::after {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 100px;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(40, 167, 69, 0.1));
                transform: skewX(-15deg);
                transition: all 0.3s ease;
            }
            
            .voyage-card:hover::after {
                transform: skewX(-15deg) translateX(10px);
            }
            
            /* Prix avec effet 3D */
            .price-badge { 
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                color: white; 
                border-radius: 25px; 
                padding: 12px 20px; 
                font-weight: bold;
                box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            .price-badge::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                transition: left 0.5s ease;
            }
            
            .price-badge:hover::before {
                left: 100%;
            }
            
            /* Boutons avec animations fluides */
            .btn-reserve { 
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%); 
                border: none; 
                border-radius: 25px; 
                color: white; 
                font-weight: bold;
                padding: 12px 24px;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            .btn-reserve:hover { 
                background: linear-gradient(135deg, #ff5252 0%, #ff7979 100%); 
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
            }
            
            .btn-reserve::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                background: rgba(255,255,255,0.3);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                transition: width 0.3s ease, height 0.3s ease;
            }
            
            .btn-reserve:active::after {
                width: 300px;
                height: 300px;
            }
            
            /* Badge Orange Money avec animation */
            .orange-money-badge { 
                background: linear-gradient(135deg, #6c5ce7, #a29bfe); 
                color: white; 
                padding: 8px 16px; 
                border-radius: 20px; 
                font-size: 0.9em;
                box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3);
                animation: pulse 2s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            /* Icônes avec animations */
            .fas, .fab {
                transition: all 0.3s ease;
            }
            
            .card:hover .fas,
            .card:hover .fab {
                transform: scale(1.1);
                color: #667eea;
            }
            
            /* Filtres avec effet glassmorphism */
            .form-control, .form-select {
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.2);
                background: rgba(255,255,255,0.9);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            
            .form-control:focus, .form-select:focus {
                border-color: #667eea;
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
                background: rgba(255,255,255,1);
            }
            
            /* Loading avec animation personnalisée */
            .loading-spinner {
                display: inline-block;
                width: 40px;
                height: 40px;
                border: 3px solid rgba(102, 126, 234, 0.3);
                border-radius: 50%;
                border-top-color: #667eea;
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            /* Badges avec effet néon */
            .badge {
                padding: 8px 12px;
                border-radius: 15px;
                font-weight: 500;
                text-shadow: 0 1px 3px rgba(0,0,0,0.3);
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                to { box-shadow: 0 0 20px rgba(0,0,0,0.2); }
            }
            
            /* Conteneur principal avec animation d'entrée */
            .container {
                animation: fadeInUp 0.8s ease-out;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Section mes réservations avec style premium */
            #myBookingsSection {
                animation: slideInRight 0.6s ease-out;
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            /* Modals avec effet de zoom */
            .modal-content {
                border-radius: 20px;
                border: none;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                animation: modalZoom 0.3s ease-out;
            }
            
            @keyframes modalZoom {
                from {
                    opacity: 0;
                    transform: scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            .modal-header {
                border-bottom: none;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border-radius: 20px 20px 0 0;
            }
            
            /* Responsive improvements */
            @media (max-width: 768px) {
                .card {
                    margin-bottom: 15px;
                }
                
                .voyage-card .row {
                    text-align: center;
                }
                
                .price-badge {
                    margin: 10px 0;
                }
            }
            
            /* Scrollbar personnalisée */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #5a6fd8, #6a5acd);
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light fixed-top">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <i class="fas fa-shield-alt text-primary"></i>
                    <strong>RoadShield Travel</strong>
                </a>
                <div class="navbar-nav ms-auto">
                    <div class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user"></i> <span id="userName">Client</span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" onclick="showMyBookings()">
                                <i class="fas fa-ticket-alt"></i> Mes Réservations</a></li>
                            <li><a class="dropdown-item" href="#" onclick="showModifyBookings()">
                                <i class="fas fa-edit"></i> Modifier mes Voyages</a></li>
                            <li><a class="dropdown-item" href="#" onclick="showPaymentHistory()">
                                <i class="fas fa-credit-card"></i> Historique Paiements</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="#" onclick="logout()">
                                <i class="fas fa-sign-out-alt"></i> Déconnexion</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="container" style="margin-top: 100px;">
            
            <!-- Welcome Section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-body text-center">
                            <h2><i class="fas fa-bus text-primary"></i> Bienvenue chez RoadShield Travel</h2>
                            <p class="lead">Réservez vos voyages en toute sécurité à travers le Cameroun</p>
                            <div class="orange-money-badge">
                                <i class="fab fa-stripe"></i> Paiement Stripe sécurisé
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Search Filters -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-search"></i> Rechercher un Voyage</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3 mb-3">
                                    <label class="form-label">Ville de Départ</label>
                                    <select class="form-select" id="filterDeparture">
                                        <option value="">Toutes les villes</option>
                                        <option value="Yaoundé">Yaoundé</option>
                                        <option value="Douala">Douala</option>
                                        <option value="Bafoussam">Bafoussam</option>
                                        <option value="Bamenda">Bamenda</option>
                                        <option value="Garoua">Garoua</option>
                                        <option value="Maroua">Maroua</option>
                                    </select>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <label class="form-label">Ville d'Arrivée</label>
                                    <select class="form-select" id="filterArrival">
                                        <option value="">Toutes les villes</option>
                                        <option value="Yaoundé">Yaoundé</option>
                                        <option value="Douala">Douala</option>
                                        <option value="Bafoussam">Bafoussam</option>
                                        <option value="Bamenda">Bamenda</option>
                                        <option value="Garoua">Garoua</option>
                                        <option value="Maroua">Maroua</option>
                                    </select>
                                </div>
                                <div class="col-md-2 mb-3">
                                    <label class="form-label">Date</label>
                                    <input type="date" class="form-control" id="filterDate">
                                </div>
                                <div class="col-md-2 mb-3">
                                    <label class="form-label">Prix Max</label>
                                    <input type="number" class="form-control" id="filterPrice" placeholder="XAF">
                                </div>
                                <div class="col-md-2 mb-3">
                                    <label class="form-label">&nbsp;</label>
                                    <button class="btn btn-primary w-100" onclick="filterTrips()">
                                        <i class="fas fa-search"></i> Rechercher
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Available Trips -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5><i class="fas fa-route"></i> Voyages Disponibles</h5>
                            <button class="btn btn-outline-primary btn-sm" onclick="loadAvailableTrips()">
                                <i class="fas fa-sync-alt"></i> Actualiser
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="tripsContainer">
                                <div class="text-center">
                                    <div class="loading-spinner"></div>
                                    <p style="margin-top: 20px; color: #667eea; font-weight: 600;">Chargement des voyages disponibles...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section Mes Réservations -->
        <div id="myBookingsSection" class="container" style="margin-top: 100px; display: none;">
            <div class="card">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5><i class="fas fa-ticket-alt"></i> Mes Réservations</h5>
                        <button class="btn btn-primary" onclick="backToTrips()">
                            <i class="fas fa-arrow-left"></i> Retour aux Voyages
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div id="myBookingsContent">
                        <div class="text-center">
                            <i class="fas fa-spinner fa-spin fa-2x text-primary"></i>
                            <p>Chargement de vos réservations...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal Modifier Réservation -->
        <div class="modal fade" id="modifyBookingModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-edit"></i> Modifier ma Réservation
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="modifyBookingContent"></div>
                        
                        <form id="modifyBookingForm" style="display: none;">
                            <div class="alert alert-info">
                                <i class="fas fa-info-circle"></i>
                                <strong>Modification gratuite :</strong> Vous pouvez modifier votre réservation jusqu'à 24h avant le départ.
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nouveau Voyage</label>
                                    <select class="form-select" id="newTripSelect" onchange="updateModificationCost()">
                                        <option value="">Sélectionner un nouveau voyage...</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nombre de Places</label>
                                    <select class="form-select" id="newSeatsSelect" onchange="updateModificationCost()">
                                        <option value="1">1 Place</option>
                                        <option value="2">2 Places</option>
                                        <option value="3">3 Places</option>
                                        <option value="4">4 Places</option>
                                        <option value="5">5 Places</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Type de Voyage</label>
                                <select class="form-select" id="newTripTypeSelect" onchange="updateModificationCost()">
                                    <option value="aller">Aller Simple</option>
                                    <option value="retour">Aller-Retour</option>
                                </select>
                            </div>
                            
                            <div class="card border-primary">
                                <div class="card-header bg-primary text-white">
                                    <h6 class="mb-0">Résumé de la Modification</h6>
                                </div>
                                <div class="card-body">
                                    <div id="modificationSummary"></div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Annuler
                        </button>
                        <button type="button" class="btn btn-success" id="confirmModificationBtn" onclick="confirmModification()" style="display: none;">
                            <i class="fas fa-check"></i> Confirmer la Modification
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de Réservation -->
        <div class="modal fade" id="bookingModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-ticket-alt"></i> Réserver ce Voyage
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="bookingDetails"></div>
                        
                        <form id="bookingForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nombre de Places *</label>
                                    <select class="form-select" name="seats" required onchange="updatePaymentInfo()">
                                        <option value="1">1 Place</option>
                                        <option value="2">2 Places</option>
                                        <option value="3">3 Places</option>
                                        <option value="4">4 Places</option>
                                        <option value="5">5 Places</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Type de Voyage *</label>
                                    <select class="form-select" name="trip_type" required onchange="updatePaymentInfo()">
                                        <option value="aller">Aller Simple</option>
                                        <option value="retour">Aller-Retour</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Informations de Paiement *</label>
                                <div class="card border-primary">
                                    <div class="card-header bg-primary text-white">
                                        <i class="fab fa-stripe"></i> Paiement Sécurisé par Stripe
                                    </div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">Numéro de Carte</label>
                                                <input type="text" class="form-control" name="card_number" 
                                                       placeholder="4242 4242 4242 4242" maxlength="19" required>
                                                <small class="text-muted">Utilisez 4242 4242 4242 4242 pour les tests</small>
                                            </div>
                                            <div class="col-md-3 mb-3">
                                                <label class="form-label">MM/AA</label>
                                                <input type="text" class="form-control" name="card_expiry" 
                                                       placeholder="12/25" maxlength="5" required>
                                            </div>
                                            <div class="col-md-3 mb-3">
                                                <label class="form-label">CVC</label>
                                                <input type="text" class="form-control" name="card_cvc" 
                                                       placeholder="123" maxlength="4" required>
                                            </div>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Nom sur la Carte</label>
                                            <input type="text" class="form-control" name="card_name" 
                                                   placeholder="Jean Dupont" required>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Email de Facturation</label>
                                            <input type="email" class="form-control" name="billing_email" 
                                                   placeholder="jean@example.com" required>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="alert alert-info">
                                <h6><i class="fas fa-calculator"></i> Récapitulatif du Paiement</h6>
                                <div id="paymentInfo"></div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Annuler
                        </button>
                        <button type="button" class="btn btn-reserve" onclick="processBooking()">
                            <i class="fab fa-stripe"></i> Payer avec Stripe
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de Facture -->
        <div class="modal fade" id="invoiceModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-receipt"></i> Facture de Voyage
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="invoiceContent"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" onclick="downloadInvoice()">
                            <i class="fas fa-download"></i> Télécharger PDF
                        </button>
                        <button type="button" class="btn btn-success" onclick="sendInvoiceBySMS()">
                            <i class="fas fa-sms"></i> Envoyer par SMS
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            class TravelClient {
                constructor() {
                    this.trips = [];
                    this.currentBooking = null;
                    this.userBookings = JSON.parse(localStorage.getItem('userBookings') || '[]');
                    this.init();
                }

                init() {
                    this.checkAuth();
                    this.loadAvailableTrips();
                }

                checkAuth() {
                    const token = localStorage.getItem('authToken');
                    const user = JSON.parse(localStorage.getItem('userInfo') || 'null');
                    
                    if (!token || !user || user.role !== 'client') {
                        window.location.href = '/login/';
                        return;
                    }
                    
                    document.getElementById('userName').textContent = user.first_name + ' ' + user.last_name;
                }

                loadAvailableTrips() {
                    // Récupérer les voyages créés par l'admin
                    this.trips = JSON.parse(localStorage.getItem('trips') || '[]');
                    this.displayTrips(this.trips);
                }

                displayTrips(trips) {
                    const container = document.getElementById('tripsContainer');
                    
                    if (!trips || trips.length === 0) {
                        container.innerHTML = `
                            <div class="text-center">
                                <i class="fas fa-exclamation-triangle fa-2x text-warning"></i>
                                <p>Aucun voyage disponible pour le moment.</p>
                                <small class="text-muted">Les administrateurs doivent programmer des voyages depuis leur interface.</small>
                            </div>
                        `;
                        return;
                    }

                    // Filtrer les voyages futurs seulement
                    const futureTrips = trips.filter(trip => new Date(trip.date) >= new Date().setHours(0,0,0,0));
                    
                    if (futureTrips.length === 0) {
                        container.innerHTML = `
                            <div class="text-center">
                                <i class="fas fa-calendar-times fa-2x text-info"></i>
                                <p>Aucun voyage futur disponible.</p>
                            </div>
                        `;
                        return;
                    }

                    const tripsHtml = futureTrips.map(trip => this.createTripCard(trip)).join('');
                    container.innerHTML = tripsHtml;
                }

                createTripCard(trip) {
                    const availableSeats = trip.available_seats - this.getBookedSeats(trip.id);
                    const statusBadge = availableSeats > 0 ? 
                        `<span class="badge bg-success">${availableSeats} places disponibles</span>` :
                        `<span class="badge bg-danger">Complet</span>`;

                    return `
                        <div class="voyage-card card mb-3" style="animation: slideInUp 0.6s ease-out; animation-delay: ${Math.random() * 0.3}s;">
                            <div class="card-body" style="position: relative;">
                                <div class="row align-items-center">
                                    <div class="col-md-3">
                                        <div style="position: relative;">
                                            <h6 class="mb-1" style="display: flex; align-items: center;">
                                                <i class="fas fa-map-marker-alt text-success" style="margin-right: 8px; animation: bounce 2s infinite;"></i>
                                                ${trip.departure_city}
                                            </h6>
                                            <small class="text-muted" style="font-weight: 500;">${trip.departure_time}</small>
                                            
                                            <div class="my-2" style="display: flex; align-items: center; justify-content: center;">
                                                <i class="fas fa-arrow-down text-primary" style="animation: moveDown 2s ease-in-out infinite;"></i>
                                                <small class="text-muted" style="margin-left: 8px;">${trip.duration || 'N/A'}</small>
                                            </div>
                                            
                                            <h6 class="mb-1" style="display: flex; align-items: center;">
                                                <i class="fas fa-map-marker-alt text-danger" style="margin-right: 8px;"></i>
                                                ${trip.arrival_city}
                                            </h6>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-2">
                                        <div class="text-center" style="padding: 15px;">
                                            <i class="fas fa-calendar text-primary" style="font-size: 1.5rem; margin-bottom: 8px;"></i>
                                            <div class="fw-bold" style="color: #667eea;">${new Date(trip.date).toLocaleDateString('fr-FR')}</div>
                                            <small class="text-muted">Bus ${trip.bus_id}</small>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-2">
                                        <div class="text-center">
                                            <i class="fas fa-users text-info" style="font-size: 1.3rem; margin-bottom: 8px;"></i>
                                            <div>${statusBadge}</div>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-3">
                                        <div class="text-center" style="padding: 10px;">
                                            <div class="price-badge mb-2" style="display: inline-block;">
                                                ${trip.price_simple.toLocaleString()} XAF
                                            </div>
                                            <small class="text-muted d-block">Aller simple</small>
                                            <small class="text-success d-block" style="font-weight: 600;">
                                                Aller-retour: ${trip.price_return.toLocaleString()} XAF
                                            </small>
                                        </div>
                                    </div>
                                    
                                    <div class="col-md-2">
                                        ${availableSeats > 0 ? 
                                            `<button class="btn btn-reserve w-100" onclick="travelClient.openBookingModal('${trip.id}')" style="position: relative; z-index: 2;">
                                                <i class="fas fa-ticket-alt"></i> Réserver
                                            </button>` :
                                            `<button class="btn btn-secondary w-100" disabled style="opacity: 0.6;">
                                                <i class="fas fa-ban"></i> Complet
                                            </button>`
                                        }
                                    </div>
                                </div>
                                
                                ${trip.notes ? `<div class="mt-2" style="border-top: 1px solid rgba(0,0,0,0.1); padding-top: 10px;"><small class="text-muted"><i class="fas fa-info-circle" style="color: #667eea;"></i> ${trip.notes}</small></div>` : ''}
                            </div>
                            <style>
                                @keyframes slideInUp {
                                    from {
                                        opacity: 0;
                                        transform: translateY(30px);
                                    }
                                    to {
                                        opacity: 1;
                                        transform: translateY(0);
                                    }
                                }
                                
                                @keyframes bounce {
                                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                                    40% { transform: translateY(-5px); }
                                    60% { transform: translateY(-3px); }
                                }
                                
                                @keyframes moveDown {
                                    0%, 100% { transform: translateY(0); }
                                    50% { transform: translateY(5px); }
                                }
                            </style>
                        </div>
                    `;
                }

                getBookedSeats(tripId) {
                    return this.userBookings
                        .filter(booking => booking.trip_id == tripId)
                        .reduce((total, booking) => total + booking.seats, 0);
                }

                openBookingModal(tripId) {
                    const trip = this.trips.find(t => t.id == tripId);
                    if (!trip) return;
                    
                    this.currentBooking = trip;
                    
                    const details = `
                        <div class="row">
                            <div class="col-md-6">
                                <h6><i class="fas fa-route"></i> Détails du Voyage</h6>
                                <p><strong>${trip.departure_city}</strong> → <strong>${trip.arrival_city}</strong></p>
                                <p><i class="fas fa-clock"></i> ${trip.departure_time} ${trip.duration ? '(' + trip.duration + ')' : ''}</p>
                                <p><i class="fas fa-calendar"></i> ${new Date(trip.date).toLocaleDateString('fr-FR')}</p>
                            </div>
                            <div class="col-md-6">
                                <h6><i class="fas fa-bus"></i> Informations Transport</h6>
                                <p>Bus: <strong>${trip.bus_id}</strong></p>
                                <p>Places totales: <strong>${trip.available_seats}</strong></p>
                                <p>Places disponibles: <strong>${trip.available_seats - this.getBookedSeats(trip.id)}</strong></p>
                            </div>
                        </div>
                    `;
                    
                    document.getElementById('bookingDetails').innerHTML = details;
                    this.updatePaymentInfo();
                    
                    new bootstrap.Modal(document.getElementById('bookingModal')).show();
                }

                updatePaymentInfo() {
                    if (!this.currentBooking) return;
                    
                    const form = document.getElementById('bookingForm');
                    const seats = parseInt(form.seats.value) || 1;
                    const tripType = form.trip_type.value || 'aller';
                    
                    const pricePerSeat = tripType === 'retour' ? this.currentBooking.price_return : this.currentBooking.price_simple;
                    const subtotal = pricePerSeat * seats;
                    const stripeFees = Math.round(subtotal * 0.029 + 30); // Frais Stripe: 2.9% + 30 XAF
                    const total = subtotal + stripeFees;
                    
                    const paymentInfo = `
                        <div class="row">
                            <div class="col-6">
                                <strong>Places:</strong> ${seats}
                            </div>
                            <div class="col-6">
                                <strong>Type:</strong> ${tripType === 'retour' ? 'Aller-Retour' : 'Aller Simple'}
                            </div>
                            <div class="col-6">
                                <strong>Prix unitaire:</strong> ${pricePerSeat.toLocaleString()} XAF
                            </div>
                            <div class="col-6">
                                <strong>Sous-total:</strong> ${subtotal.toLocaleString()} XAF
                            </div>
                            <div class="col-6">
                                <strong>Frais Stripe:</strong> ${stripeFees.toLocaleString()} XAF
                            </div>
                            <div class="col-6">
                                <strong>Total à payer:</strong> <span class="text-success fw-bold">${total.toLocaleString()} XAF</span>
                            </div>
                        </div>
                    `;
                    
                    document.getElementById('paymentInfo').innerHTML = paymentInfo;
                }

                async processBooking() {
                    const form = document.getElementById('bookingForm');
                    const formData = new FormData(form);
                    
                    if (!form.checkValidity()) {
                        form.classList.add('was-validated');
                        return;
                    }
                    
                    // Afficher l'indicateur de chargement
                    const payButton = document.querySelector('.btn-reserve');
                    const originalText = payButton.innerHTML;
                    payButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Traitement...';
                    payButton.disabled = true;
                    
                    try {
                        // Valider les informations de carte
                        const cardNumber = formData.get('card_number').replace(/\s/g, '');
                        const cardExpiry = formData.get('card_expiry');
                        const cardCvc = formData.get('card_cvc');
                        const cardName = formData.get('card_name');
                        const billingEmail = formData.get('billing_email');
                        
                        if (!this.validateStripeCard(cardNumber, cardExpiry, cardCvc)) {
                            alert('Informations de carte invalides. Utilisez 4242424242424242 pour les tests.');
                            return;
                        }
                        
                        const seats = parseInt(formData.get('seats'));
                        const tripType = formData.get('trip_type');
                        const pricePerSeat = tripType === 'retour' ? this.currentBooking.price_return : this.currentBooking.price_simple;
                        const subtotal = pricePerSeat * seats;
                        const stripeFees = Math.round(subtotal * 0.029 + 30);
                        const total = subtotal + stripeFees;
                        
                        // Simuler le paiement Stripe
                        const paymentResult = await this.processStripePayment({
                            cardNumber, cardExpiry, cardCvc, cardName, billingEmail, amount: total
                        });
                        
                        if (paymentResult.success) {
                            const booking = this.createBooking(seats, tripType, total, paymentResult);
                            this.showInvoice(booking);
                            
                            // Fermer le modal de réservation
                            bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();
                        } else {
                            alert('Erreur lors du paiement Stripe: ' + paymentResult.error);
                        }
                        
                    } catch (error) {
                        console.error('Erreur:', error);
                        alert('Erreur lors du traitement du paiement');
                    } finally {
                        // Restaurer le bouton
                        payButton.innerHTML = originalText;
                        payButton.disabled = false;
                    }
                }

                validateStripeCard(cardNumber, expiry, cvc) {
                    // Validation basique pour Stripe
                    if (cardNumber.length < 13 || cardNumber.length > 19) return false;
                    if (!/^\d{2}\/\d{2}$/.test(expiry)) return false;
                    if (cvc.length < 3 || cvc.length > 4) return false;
                    
                    // Accepter les cartes de test Stripe
                    const testCards = ['4242424242424242', '4000000000000002', '5555555555554444'];
                    return testCards.includes(cardNumber) || cardNumber.startsWith('4');
                }

                async processStripePayment(paymentData) {
                    // Simulation du paiement Stripe
                    return new Promise((resolve) => {
                        setTimeout(() => {
                            // Simuler succès ou échec selon la carte
                            const success = paymentData.cardNumber !== '4000000000000002';
                            
                            if (success) {
                                resolve({
                                    success: true,
                                    payment_intent_id: `pi_${Date.now()}`,
                                    amount: paymentData.amount,
                                    currency: 'xaf',
                                    payment_method: 'card',
                                    card_brand: 'visa',
                                    card_last4: paymentData.cardNumber.slice(-4),
                                    receipt_email: paymentData.billingEmail
                                });
                            } else {
                                resolve({
                                    success: false,
                                    error: 'Carte déclinée'
                                });
                            }
                        }, 2000);
                    });
                }

                createBooking(seats, tripType, totalPrice, paymentResult) {
                    const user = JSON.parse(localStorage.getItem('userInfo'));
                    const ticketNumber = `RD${Date.now()}`;
                    
                    const booking = {
                        ticket_number: ticketNumber,
                        trip_id: this.currentBooking.id,
                        client_name: user.first_name + ' ' + user.last_name,
                        client_email: paymentResult.receipt_email,
                        route: `${this.currentBooking.departure_city} → ${this.currentBooking.arrival_city}`,
                        date: this.currentBooking.date,
                        departure_time: this.currentBooking.departure_time,
                        bus_id: this.currentBooking.bus_id,
                        seats: seats,
                        trip_type: tripType,
                        total_price: totalPrice,
                        payment_method: 'Stripe',
                        payment_intent_id: paymentResult.payment_intent_id,
                        card_last4: paymentResult.card_last4,
                        card_brand: paymentResult.card_brand,
                        booking_date: new Date().toISOString(),
                        status: 'confirmed'
                    };
                    
                    // Sauvegarder la réservation
                    this.userBookings.push(booking);
                    localStorage.setItem('userBookings', JSON.stringify(this.userBookings));
                    
                    // Mettre à jour les réservations globales pour l'admin
                    const allBookings = JSON.parse(localStorage.getItem('bookings') || '[]');
                    allBookings.push(booking);
                    localStorage.setItem('bookings', JSON.stringify(allBookings));
                    
                    return booking;
                }

                showInvoice(booking) {
                    const trip = this.currentBooking;
                    const invoiceHtml = `
                        <div class="invoice">
                            <div class="text-center mb-4">
                                <h3><i class="fas fa-shield-alt text-success"></i> RoadShield Travel</h3>
                                <p class="text-muted">Facture de Voyage</p>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Informations Client</h6>
                                    <p>
                                        <strong>Nom:</strong> ${booking.client_name}<br>
                                        <strong>Email:</strong> ${booking.client_email}<br>
                                        <strong>N° Ticket:</strong> ${booking.ticket_number}
                                    </p>
                                </div>
                                <div class="col-md-6">
                                    <h6>Détails du Voyage</h6>
                                    <p>
                                        <strong>Route:</strong> ${booking.route}<br>
                                        <strong>Date:</strong> ${new Date(booking.date).toLocaleDateString('fr-FR')}<br>
                                        <strong>Départ:</strong> ${booking.departure_time}<br>
                                        <strong>Bus:</strong> ${booking.bus_id}
                                    </p>
                                </div>
                            </div>
                            
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <thead class="table-light">
                                        <tr>
                                            <th>Description</th>
                                            <th>Quantité</th>
                                            <th>Prix Unitaire</th>
                                            <th>Total</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Voyage ${booking.trip_type === 'retour' ? 'Aller-Retour' : 'Aller Simple'}</td>
                                            <td>${booking.seats}</td>
                                            <td>${(booking.trip_type === 'retour' ? trip.price_return : trip.price_simple).toLocaleString()} XAF</td>
                                            <td>${(booking.seats * (booking.trip_type === 'retour' ? trip.price_return : trip.price_simple)).toLocaleString()} XAF</td>
                                        </tr>
                                        <tr>
                                            <td>Frais de Transaction Stripe (2.9% + 30 XAF)</td>
                                            <td>1</td>
                                            <td>${Math.round(booking.total_price * 0.029 + 30).toLocaleString()} XAF</td>
                                            <td>${Math.round(booking.total_price * 0.029 + 30).toLocaleString()} XAF</td>
                                        </tr>
                                    </tbody>
                                    <tfoot class="table-success">
                                        <tr>
                                            <th colspan="3">Total Payé</th>
                                            <th>${booking.total_price.toLocaleString()} XAF</th>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Paiement Stripe</h6>
                                    <p>
                                        <strong>Méthode:</strong> Carte bancaire<br>
                                        <strong>Carte:</strong> **** **** **** ${booking.card_last4} (${booking.card_brand.toUpperCase()})<br>
                                        <strong>ID Paiement:</strong> ${booking.payment_intent_id}<br>
                                        <strong>Statut:</strong> <span class="badge bg-success">Confirmé</span>
                                    </p>
                                </div>
                                <div class="col-md-6">
                                    <h6>Instructions</h6>
                                    <p>
                                        • Présentez ce ticket à l'embarquement<br>
                                        • Arrivez 30 minutes avant le départ<br>
                                        • Une pièce d'identité sera demandée<br>
                                        • Reçu de paiement envoyé par email
                                    </p>
                                </div>
                            </div>
                            
                            <div class="text-center mt-4 p-3 bg-light rounded">
                                <p class="mb-0"><strong>Merci de voyager avec RoadShield Travel !</strong></p>
                                <small class="text-muted">Pour toute question: +237 690 000 000 | Email: support@roadshield.cm</small>
                                <br><small class="text-muted">Paiement sécurisé par Stripe - Transaction ID: ${booking.payment_intent_id}</small>
                            </div>
                        </div>
                    `;
                    
                    document.getElementById('invoiceContent').innerHTML = invoiceHtml;
                    new bootstrap.Modal(document.getElementById('invoiceModal')).show();
                }

                loadMyBookings() {
                    const user = JSON.parse(localStorage.getItem('userInfo'));
                    const myBookings = this.userBookings.filter(booking => 
                        booking.client_name === `${user.first_name} ${user.last_name}`
                    );

                    if (myBookings.length === 0) {
                        document.getElementById('myBookingsContent').innerHTML = `
                            <div class="text-center" style="padding: 60px 20px;">
                                <div style="animation: float 3s ease-in-out infinite;">
                                    <i class="fas fa-ticket-alt fa-4x text-muted mb-4"></i>
                                </div>
                                <h5 style="color: #667eea; margin-bottom: 15px;">Aucune réservation</h5>
                                <p class="text-muted" style="margin-bottom: 30px;">Vous n'avez pas encore effectué de réservation.</p>
                                <button class="btn btn-primary btn-lg" onclick="backToTrips()" style="animation: pulse 2s ease-in-out infinite;">
                                    <i class="fas fa-plus"></i> Réserver un Voyage
                                </button>
                                <style>
                                    @keyframes float {
                                        0%, 100% { transform: translateY(0px); }
                                        50% { transform: translateY(-10px); }
                                    }
                                </style>
                            </div>
                        `;
                        return;
                    }

                    const bookingsHtml = myBookings.map((booking, index) => {
                        const canModify = this.canModifyBooking(booking);
                        const modifyButton = canModify ? 
                            `<button class="btn btn-warning btn-sm" onclick="travelClient.openModifyModal('${booking.ticket_number}')">
                                <i class="fas fa-edit"></i> Modifier
                            </button>` :
                            `<button class="btn btn-secondary btn-sm" disabled title="Modification non autorisée">
                                <i class="fas fa-lock"></i> Verrouillé
                            </button>`;

                        return `
                            <div class="card mb-3">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <h6 class="card-title">
                                                <i class="fas fa-ticket-alt text-primary"></i>
                                                Ticket: ${booking.ticket_number}
                                            </h6>
                                            <p class="mb-1"><strong>Route:</strong> ${booking.route}</p>
                                            <p class="mb-1"><strong>Date:</strong> ${new Date(booking.date).toLocaleDateString('fr-FR')} à ${booking.departure_time}</p>
                                            <p class="mb-1"><strong>Places:</strong> ${booking.seats} (${booking.trip_type === 'retour' ? 'Aller-Retour' : 'Aller Simple'})</p>
                                            <p class="mb-1"><strong>Bus:</strong> ${booking.bus_id}</p>
                                            <p class="mb-0"><strong>Montant:</strong> ${booking.total_price.toLocaleString()} XAF</p>
                                        </div>
                                        <div class="col-md-4 text-end">
                                            <div class="mb-2">
                                                ${this.getBookingStatusBadge(booking.status)}
                                            </div>
                                            <div class="btn-group-vertical">
                                                ${modifyButton}
                                                <button class="btn btn-info btn-sm" onclick="travelClient.viewBookingDetails('${booking.ticket_number}')">
                                                    <i class="fas fa-eye"></i> Détails
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('');

                    document.getElementById('myBookingsContent').innerHTML = bookingsHtml;
                }

                canModifyBooking(booking) {
                    // Peut modifier si confirmé et si plus de 24h avant le départ
                    if (booking.status !== 'confirmed') return false;
                    
                    const departureDate = new Date(`${booking.date} ${booking.departure_time}`);
                    const now = new Date();
                    const hoursDifference = (departureDate - now) / (1000 * 60 * 60);
                    
                    return hoursDifference > 24;
                }

                getBookingStatusBadge(status) {
                    const badges = {
                        'confirmed': '<span class="badge bg-success">Confirmée</span>',
                        'validated': '<span class="badge bg-primary">Validée - Embarqué</span>',
                        'cancelled': '<span class="badge bg-secondary">Annulée</span>',
                        'refunded': '<span class="badge bg-warning">Remboursée</span>',
                        'modified': '<span class="badge bg-info">Modifiée</span>'
                    };
                    return badges[status] || '<span class="badge bg-light">Inconnu</span>';
                }

                openModifyModal(ticketNumber) {
                    const booking = this.userBookings.find(b => b.ticket_number === ticketNumber);
                    if (!booking) return;

                    this.currentModifyBooking = booking;
                    
                    // Afficher les détails de la réservation actuelle
                    document.getElementById('modifyBookingContent').innerHTML = `
                        <div class="card border-primary mb-3">
                            <div class="card-header bg-primary text-white">
                                <h6 class="mb-0">Réservation Actuelle</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-6">
                                        <strong>Ticket:</strong> ${booking.ticket_number}<br>
                                        <strong>Route:</strong> ${booking.route}<br>
                                        <strong>Date:</strong> ${new Date(booking.date).toLocaleDateString('fr-FR')}
                                    </div>
                                    <div class="col-6">
                                        <strong>Heure:</strong> ${booking.departure_time}<br>
                                        <strong>Places:</strong> ${booking.seats}<br>
                                        <strong>Montant:</strong> ${booking.total_price.toLocaleString()} XAF
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;

                    // Charger les voyages disponibles pour modification
                    this.loadAvailableTripsForModification();
                    
                    document.getElementById('modifyBookingForm').style.display = 'block';
                    new bootstrap.Modal(document.getElementById('modifyBookingModal')).show();
                }

                loadAvailableTripsForModification() {
                    const select = document.getElementById('newTripSelect');
                    const futureTrips = this.trips.filter(trip => new Date(trip.date) > new Date());
                    
                    const options = futureTrips.map(trip => 
                        `<option value="${trip.id}" data-trip='${JSON.stringify(trip)}'>
                            ${trip.departure_city} → ${trip.arrival_city} - ${new Date(trip.date).toLocaleDateString('fr-FR')} ${trip.departure_time}
                        </option>`
                    ).join('');
                    
                    select.innerHTML = '<option value="">Sélectionner un nouveau voyage...</option>' + options;
                }
            }

            // Fonctions globales
            function updatePaymentInfo() {
                if (window.travelClient) {
                    window.travelClient.updatePaymentInfo();
                }
            }

            function processBooking() {
                if (window.travelClient) {
                    window.travelClient.processBooking();
                }
            }

            function filterTrips() {
                // Fonction de filtrage des voyages
                alert('Fonction de filtrage en cours de développement');
            }

            function loadAvailableTrips() {
                window.travelClient.loadAvailableTrips();
            }

            function downloadInvoice() {
                const invoiceContent = document.getElementById('invoiceContent').innerHTML;
                const printWindow = window.open('', '_blank');
                printWindow.document.write(`
                    <html>
                    <head>
                        <title>Facture RoadShield Travel</title>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                        <style>
                            body { font-family: Arial, sans-serif; }
                            .invoice { max-width: 800px; margin: 20px auto; }
                            @media print { .no-print { display: none; } }
                        </style>
                    </head>
                    <body>
                        <div class="invoice">${invoiceContent}</div>
                        <div class="text-center no-print mt-3">
                            <button onclick="window.print()" class="btn btn-primary">Imprimer</button>
                            <button onclick="window.close()" class="btn btn-secondary">Fermer</button>
                        </div>
                    </body>
                    </html>
                `);
                printWindow.document.close();
            }

            function sendInvoiceBySMS() {
                alert('Facture envoyée par email à l\\'adresse de facturation !');
            }

            function showMyBookings() {
                document.querySelector('.container').style.display = 'none';
                document.getElementById('myBookingsSection').style.display = 'block';
                window.travelClient.loadMyBookings();
            }

            function showModifyBookings() {
                showMyBookings(); // Même interface, les boutons de modification sont conditionnels
            }

            function backToTrips() {
                document.querySelector('.container').style.display = 'block';
                document.getElementById('myBookingsSection').style.display = 'none';
            }

            function updateModificationCost() {
                const newTripSelect = document.getElementById('newTripSelect');
                const newSeatsSelect = document.getElementById('newSeatsSelect');
                const newTripTypeSelect = document.getElementById('newTripTypeSelect');
                
                if (!newTripSelect.value) {
                    document.getElementById('modificationSummary').innerHTML = '';
                    document.getElementById('confirmModificationBtn').style.display = 'none';
                    return;
                }
                
                const selectedOption = newTripSelect.selectedOptions[0];
                const newTrip = JSON.parse(selectedOption.dataset.trip);
                const newSeats = parseInt(newSeatsSelect.value);
                const newTripType = newTripTypeSelect.value;
                
                const currentBooking = window.travelClient.currentModifyBooking;
                
                // Calculer les nouveaux coûts
                const newPricePerSeat = newTripType === 'retour' ? newTrip.price_return : newTrip.price_simple;
                const newSubtotal = newPricePerSeat * newSeats;
                const newFees = Math.round(newSubtotal * 0.029 + 30);
                const newTotal = newSubtotal + newFees;
                
                // Calculer la différence
                const priceDifference = newTotal - currentBooking.total_price;
                const differenceText = priceDifference >= 0 ? 
                    `Supplément à payer: +${priceDifference.toLocaleString()} XAF` :
                    `Remboursement: ${Math.abs(priceDifference).toLocaleString()} XAF`;
                
                const differenceClass = priceDifference >= 0 ? 'text-warning' : 'text-success';
                
                document.getElementById('modificationSummary').innerHTML = `
                    <div class="row">
                        <div class="col-6">
                            <strong>Nouveau voyage:</strong><br>
                            ${newTrip.departure_city} → ${newTrip.arrival_city}<br>
                            ${new Date(newTrip.date).toLocaleDateString('fr-FR')} ${newTrip.departure_time}
                        </div>
                        <div class="col-6">
                            <strong>Détails:</strong><br>
                            ${newSeats} place(s) - ${newTripType === 'retour' ? 'Aller-Retour' : 'Aller Simple'}<br>
                            Nouveau total: ${newTotal.toLocaleString()} XAF
                        </div>
                    </div>
                    <hr>
                    <div class="text-center">
                        <h6 class="${differenceClass}">${differenceText}</h6>
                    </div>
                `;
                
                document.getElementById('confirmModificationBtn').style.display = 'block';
            }

            function confirmModification() {
                const newTripSelect = document.getElementById('newTripSelect');
                const newSeatsSelect = document.getElementById('newSeatsSelect');
                const newTripTypeSelect = document.getElementById('newTripTypeSelect');
                
                const selectedOption = newTripSelect.selectedOptions[0];
                const newTrip = JSON.parse(selectedOption.dataset.trip);
                const newSeats = parseInt(newSeatsSelect.value);
                const newTripType = newTripTypeSelect.value;
                
                const currentBooking = window.travelClient.currentModifyBooking;
                
                // Calculer les nouveaux coûts
                const newPricePerSeat = newTripType === 'retour' ? newTrip.price_return : newTrip.price_simple;
                const newSubtotal = newPricePerSeat * newSeats;
                const newFees = Math.round(newSubtotal * 0.029 + 30);
                const newTotal = newSubtotal + newFees;
                
                // Mettre à jour la réservation
                const bookingIndex = window.travelClient.userBookings.findIndex(b => b.ticket_number === currentBooking.ticket_number);
                if (bookingIndex !== -1) {
                    const updatedBooking = {
                        ...currentBooking,
                        trip_id: newTrip.id,
                        route: `${newTrip.departure_city} → ${newTrip.arrival_city}`,
                        date: newTrip.date,
                        departure_time: newTrip.departure_time,
                        bus_id: newTrip.bus_id,
                        seats: newSeats,
                        trip_type: newTripType,
                        total_price: newTotal,
                        status: 'confirmed',
                        modified_at: new Date().toISOString(),
                        original_booking: { ...currentBooking }
                    };
                    
                    window.travelClient.userBookings[bookingIndex] = updatedBooking;
                    localStorage.setItem('userBookings', JSON.stringify(window.travelClient.userBookings));
                    
                    // Mettre à jour aussi dans les réservations globales
                    const allBookings = JSON.parse(localStorage.getItem('bookings') || '[]');
                    const globalIndex = allBookings.findIndex(b => b.ticket_number === currentBooking.ticket_number);
                    if (globalIndex !== -1) {
                        allBookings[globalIndex] = updatedBooking;
                        localStorage.setItem('bookings', JSON.stringify(allBookings));
                    }
                    
                    // Fermer le modal et actualiser
                    bootstrap.Modal.getInstance(document.getElementById('modifyBookingModal')).hide();
                    window.travelClient.loadMyBookings();
                    
                    alert('Votre réservation a été modifiée avec succès !');
                }
            }

            function logout() {
                if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('userInfo');
                    window.location.href = '/';
                }
            }

            // Initialiser
            document.addEventListener('DOMContentLoaded', () => {
                window.travelClient = new TravelClient();
                
                // Formatage automatique des champs de carte
                const cardNumberInput = document.querySelector('input[name="card_number"]');
                const cardExpiryInput = document.querySelector('input[name="card_expiry"]');
                const cardCvcInput = document.querySelector('input[name="card_cvc"]');
                
                if (cardNumberInput) {
                    cardNumberInput.addEventListener('input', (e) => {
                        let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
                        let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
                        e.target.value = formattedValue;
                    });
                }
                
                if (cardExpiryInput) {
                    cardExpiryInput.addEventListener('input', (e) => {
                        let value = e.target.value.replace(/\D/g, '');
                        if (value.length >= 2) {
                            value = value.substring(0, 2) + '/' + value.substring(2, 4);
                        }
                        e.target.value = value;
                    });
                }
                
                if (cardCvcInput) {
                    cardCvcInput.addEventListener('input', (e) => {
                        e.target.value = e.target.value.replace(/[^0-9]/g, '');
                    });
                }
            });
        </script>
    </body>
    </html>
    """, content_type='text/html')

def serve_admin_backoffice(request):
    """Interface admin complète pour gérer tous les voyages"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>RoadShield - Administration Complète</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            .sidebar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .sidebar .nav-link {
                color: rgba(255,255,255,0.8);
                border-radius: 10px;
                margin: 5px 0;
            }
            .sidebar .nav-link:hover, .sidebar .nav-link.active {
                background: rgba(255,255,255,0.2);
                color: white;
            }
            .table-container {
                max-height: 400px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-md-3 col-lg-2 px-0">
                    <div class="sidebar p-3">
                        <h4 class="mb-4">
                            <i class="fas fa-shield-alt"></i> RoadShield
                            <div class="text-white-50 small">Administration</div>
                        </h4>
                        
                        <nav class="nav flex-column">
                            <a class="nav-link active" href="#dashboard" onclick="showSection('dashboard')">
                                <i class="fas fa-tachometer-alt"></i> Dashboard
                            </a>
                            <a class="nav-link" href="#trips" onclick="showSection('trips')">
                                <i class="fas fa-route"></i> Gestion des Voyages
                            </a>
                            <a class="nav-link" href="#buses" onclick="showSection('buses')">
                                <i class="fas fa-bus"></i> Gestion des Bus
                            </a>
                            <a class="nav-link" href="#cities" onclick="showSection('cities')">
                                <i class="fas fa-map-marker-alt"></i> Villes & Routes
                            </a>
                            <a class="nav-link" href="#bookings" onclick="showSection('bookings')">
                                <i class="fas fa-ticket-alt"></i> Réservations
                            </a>
                            <a class="nav-link" href="#payments" onclick="showSection('payments')">
                                <i class="fas fa-money-bill-wave"></i> Orange Money
                            </a>
                            <hr class="my-3">
                            <span class="text-white-50 small">
                                <i class="fas fa-user"></i> <span id="adminName">Admin</span>
                            </span>
                            <a class="nav-link" href="#" onclick="logout()">
                                <i class="fas fa-sign-out-alt"></i> Déconnexion
                            </a>
                        </nav>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-md-9 col-lg-10">
                    <div class="p-4">
                        
                        <!-- Dashboard Section -->
                        <div id="dashboard-section" class="content-section">
                            <h2><i class="fas fa-tachometer-alt text-primary"></i> Dashboard Administrateur</h2>
                            
                            <div class="row mt-4">
                                <div class="col-md-3 mb-3">
                                    <div class="card text-center border-primary">
                                        <div class="card-body">
                                            <i class="fas fa-route fa-2x text-primary mb-2"></i>
                                            <h3 class="text-primary" id="totalTrips">0</h3>
                                            <p>Voyages Programmés</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="card text-center border-success">
                                        <div class="card-body">
                                            <i class="fas fa-bus fa-2x text-success mb-2"></i>
                                            <h3 class="text-success">8</h3>
                                            <p>Bus Disponibles</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="card text-center border-warning">
                                        <div class="card-body">
                                            <i class="fas fa-ticket-alt fa-2x text-warning mb-2"></i>
                                            <h3 class="text-warning" id="totalBookings">0</h3>
                                            <p>Réservations</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <div class="card text-center border-info">
                                        <div class="card-body">
                                            <i class="fas fa-money-bill-wave fa-2x text-info mb-2"></i>
                                            <h3 class="text-info" id="totalRevenue">0</h3>
                                            <p>Revenus (XAF)</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Trips Management Section -->
                        <div id="trips-section" class="content-section" style="display: none;">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2><i class="fas fa-route text-primary"></i> Gestion Complète des Voyages</h2>
                                <button class="btn btn-success" onclick="showAddTripModal()">
                                    <i class="fas fa-plus"></i> Nouveau Voyage
                                </button>
                            </div>
                            
                            <!-- Filtres -->
                            <div class="card mb-4">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-3">
                                            <select class="form-select" id="filterStatus">
                                                <option value="">Tous les statuts</option>
                                                <option value="active">Actifs</option>
                                                <option value="completed">Terminés</option>
                                                <option value="cancelled">Annulés</option>
                                            </select>
                                        </div>
                                        <div class="col-md-3">
                                            <input type="date" class="form-control" id="filterDate">
                                        </div>
                                        <div class="col-md-4">
                                            <input type="text" class="form-control" placeholder="Rechercher route..." id="searchRoute">
                                        </div>
                                        <div class="col-md-2">
                                            <button class="btn btn-primary w-100" onclick="filterTrips()">
                                                <i class="fas fa-search"></i> Filtrer
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Table des voyages -->
                            <div class="card">
                                <div class="card-header">
                                    <h5>Tous les Voyages Programmés</h5>
                                </div>
                                <div class="card-body">
                                    <div class="table-container">
                                        <table class="table table-striped table-hover">
                                            <thead class="table-dark">
                                                <tr>
                                                    <th>ID</th>
                                                    <th>Date</th>
                                                    <th>Route</th>
                                                    <th>Horaires</th>
                                                    <th>Bus</th>
                                                    <th>Prix</th>
                                                    <th>Places</th>
                                                    <th>Statut</th>
                                                    <th>Actions</th>
                                                </tr>
                                            </thead>
                                            <tbody id="tripsTable">
                                                <!-- Les voyages seront chargés ici -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Bus Management -->
                        <div id="buses-section" class="content-section" style="display: none;">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2><i class="fas fa-bus text-success"></i> Gestion des Bus</h2>
                                <button class="btn btn-success" onclick="showAddBusModal()">
                                    <i class="fas fa-plus"></i> Nouveau Bus
                                </button>
                            </div>
                            
                            <div class="row" id="busesGrid">
                                <!-- Les bus seront chargés ici -->
                            </div>
                            
                            <div class="card mt-4">
                                <div class="card-header">
                                    <h5>Liste Complète des Bus</h5>
                                </div>
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped">
                                            <thead class="table-dark">
                                                <tr>
                                                    <th>N° Bus</th>
                                                    <th>Modèle</th>
                                                    <th>Places</th>
                                                    <th>Statut</th>
                                                    <th>Dernière Maintenance</th>
                                                    <th>Actions</th>
                                                </tr>
                                            </thead>
                                            <tbody id="busesTable">
                                                <!-- Les bus seront chargés ici -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Cities Management -->
                        <div id="cities-section" class="content-section" style="display: none;">
                            <h2><i class="fas fa-map-marker-alt text-info"></i> Villes & Routes du Cameroun</h2>
                            
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h5>Villes Principales</h5>
                                        </div>
                                        <div class="card-body">
                                            <div class="row">
                                                <div class="col-6">
                                                    <ul class="list-group list-group-flush">
                                                        <li class="list-group-item">🏛️ Yaoundé (Capitale)</li>
                                                        <li class="list-group-item">🏭 Douala (Économique)</li>
                                                        <li class="list-group-item">🏔️ Bafoussam (Ouest)</li>
                                                        <li class="list-group-item">🌿 Bamenda (Nord-Ouest)</li>
                                                    </ul>
                                                </div>
                                                <div class="col-6">
                                                    <ul class="list-group list-group-flush">
                                                        <li class="list-group-item">🌴 Garoua (Nord)</li>
                                                        <li class="list-group-item">🏜️ Maroua (Extrême-Nord)</li>
                                                        <li class="list-group-item">🌊 Kribi (Littoral)</li>
                                                        <li class="list-group-item">🌳 Bertoua (Est)</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h5>Routes Populaires</h5>
                                        </div>
                                        <div class="card-body">
                                            <div class="list-group">
                                                <div class="list-group-item d-flex justify-content-between">
                                                    <span>Yaoundé ↔ Douala</span>
                                                    <span class="badge bg-success">4h - 250km</span>
                                                </div>
                                                <div class="list-group-item d-flex justify-content-between">
                                                    <span>Douala ↔ Bafoussam</span>
                                                    <span class="badge bg-info">4h30 - 280km</span>
                                                </div>
                                                <div class="list-group-item d-flex justify-content-between">
                                                    <span>Yaoundé ↔ Bamenda</span>
                                                    <span class="badge bg-warning">6h30 - 420km</span>
                                                </div>
                                                <div class="list-group-item d-flex justify-content-between">
                                                    <span>Bafoussam ↔ Garoua</span>
                                                    <span class="badge bg-danger">9h - 580km</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Bookings Section -->
                        <div id="bookings-section" class="content-section" style="display: none;">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2><i class="fas fa-ticket-alt text-warning"></i> Gestion des Réservations</h2>
                                <div>
                                    <button class="btn btn-primary" onclick="showTicketValidationModal()">
                                        <i class="fas fa-qrcode"></i> Valider par N° Ticket
                                    </button>
                                    <button class="btn btn-outline-primary" onclick="refreshBookings()">
                                        <i class="fas fa-sync-alt"></i> Actualiser
                                    </button>
                                </div>
                            </div>
                            
                            <!-- Filtres des réservations -->
                            <div class="card mb-4">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-3">
                                            <select class="form-select" id="filterBookingStatus">
                                                <option value="">Tous les statuts</option>
                                                <option value="confirmed">Confirmées</option>
                                                <option value="validated">Validées (Embarquement)</option>
                                                <option value="cancelled">Annulées</option>
                                                <option value="refunded">Remboursées</option>
                                            </select>
                                        </div>
                                        <div class="col-md-3">
                                            <input type="date" class="form-control" id="filterBookingDate">
                                        </div>
                                        <div class="col-md-4">
                                            <input type="text" class="form-control" placeholder="Rechercher par nom, ticket..." id="searchBooking">
                                        </div>
                                        <div class="col-md-2">
                                            <button class="btn btn-primary w-100" onclick="filterBookings()">
                                                <i class="fas fa-search"></i> Filtrer
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <h5>Toutes les Réservations</h5>
                                        <div class="d-flex gap-2">
                                            <span class="badge bg-success" id="confirmedCount">0 Confirmées</span>
                                            <span class="badge bg-primary" id="validatedCount">0 Validées</span>
                                            <span class="badge bg-secondary" id="cancelledCount">0 Annulées</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="table-container">
                                        <table class="table table-striped table-hover">
                                            <thead class="table-dark">
                                                <tr>
                                                    <th>N° Ticket</th>
                                                    <th>Client</th>
                                                    <th>Voyage</th>
                                                    <th>Date/Heure</th>
                                                    <th>Places</th>
                                                    <th>Montant</th>
                                                    <th>Statut</th>
                                                    <th>Actions</th>
                                                </tr>
                                            </thead>
                                            <tbody id="bookingsTable">
                                                <!-- Les réservations seront chargées ici -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Payments Section -->
                        <div id="payments-section" class="content-section" style="display: none;">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2><i class="fas fa-money-bill-wave text-info"></i> Rapports Financiers</h2>
                                <button class="btn btn-primary" onclick="generateFinancialReport()">
                                    <i class="fas fa-chart-line"></i> Générer Rapport
                                </button>
                            </div>
                            
                            <!-- Filtres de période -->
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5>Filtres de Période</h5>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-3">
                                            <label class="form-label">Date de début</label>
                                            <input type="date" class="form-control" id="reportStartDate">
                                        </div>
                                        <div class="col-md-3">
                                            <label class="form-label">Date de fin</label>
                                            <input type="date" class="form-control" id="reportEndDate">
                                        </div>
                                        <div class="col-md-3">
                                            <label class="form-label">Période prédéfinie</label>
                                            <select class="form-select" id="predefinedPeriod" onchange="setPredefinedPeriod()">
                                                <option value="">Personnalisée</option>
                                                <option value="today">Aujourd'hui</option>
                                                <option value="week">Cette semaine</option>
                                                <option value="month">Ce mois</option>
                                                <option value="quarter">Ce trimestre</option>
                                                <option value="year">Cette année</option>
                                            </select>
                                        </div>
                                        <div class="col-md-3 d-flex align-items-end">
                                            <button class="btn btn-primary w-100" onclick="updateFinancialReport()">
                                                <i class="fas fa-refresh"></i> Actualiser
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Résumé financier -->
                            <div class="row mb-4" id="financialSummary">
                                <div class="col-md-3">
                                    <div class="card text-center border-success">
                                        <div class="card-body">
                                            <h4 class="text-success" id="totalRevenueReport">0</h4>
                                            <p>Revenus Totaux (XAF)</p>
                                            <small class="text-muted" id="revenueChange"></small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card text-center border-primary">
                                        <div class="card-body">
                                            <h4 class="text-primary" id="totalTicketsSold">0</h4>
                                            <p>Places Vendues</p>
                                            <small class="text-muted" id="ticketsChange"></small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card text-center border-warning">
                                        <div class="card-body">
                                            <h4 class="text-warning" id="totalRefunds">0</h4>
                                            <p>Remboursements (XAF)</p>
                                            <small class="text-muted" id="refundsChange"></small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card text-center border-info">
                                        <div class="card-body">
                                            <h4 class="text-info" id="netRevenue">0</h4>
                                            <p>Revenus Nets (XAF)</p>
                                            <small class="text-muted" id="netChange"></small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Détails par statut -->
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6>Répartition par Statut</h6>
                                        </div>
                                        <div class="card-body">
                                            <div id="statusBreakdown"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6>Top Routes</h6>
                                        </div>
                                        <div class="card-body">
                                            <div id="topRoutes"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Tableau détaillé des transactions -->
                            <div class="card">
                                <div class="card-header">
                                    <h5>Détail des Transactions</h5>
                                </div>
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped">
                                            <thead class="table-dark">
                                                <tr>
                                                    <th>Date</th>
                                                    <th>Ticket</th>
                                                    <th>Client</th>
                                                    <th>Route</th>
                                                    <th>Places</th>
                                                    <th>Montant</th>
                                                    <th>Statut</th>
                                                    <th>Impact Revenus</th>
                                                </tr>
                                            </thead>
                                            <tbody id="transactionsTable">
                                                <!-- Les transactions seront chargées ici -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Modal Validation Ticket -->
        <div class="modal fade" id="ticketValidationModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-qrcode"></i> Validation de Ticket
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Numéro de Ticket</label>
                            <input type="text" class="form-control" id="ticketNumberInput" 
                                   placeholder="Ex: RD1703123456789" onkeyup="searchTicketByNumber()">
                            <div class="form-text">
                                <i class="fas fa-info-circle"></i>
                                Scannez le QR code ou saisissez le numéro manuellement
                            </div>
                        </div>
                        
                        <div id="ticketSearchResult"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Modal Confirmation Action -->
        <div class="modal fade" id="confirmActionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="confirmActionTitle">
                            Confirmer l'Action
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="confirmActionContent"></div>
                        
                        <div class="mt-3" id="emailNotificationSection" style="display: none;">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="sendEmailConfirmation" checked>
                                <label class="form-check-label" for="sendEmailConfirmation">
                                    Envoyer un email de confirmation au client
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Annuler
                        </button>
                        <button type="button" class="btn" id="confirmActionButton">
                            Confirmer
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Modal Nouveau Bus -->
        <div class="modal fade" id="addBusModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-bus"></i> Ajouter un Nouveau Bus
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addBusForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Numéro du Bus *</label>
                                    <input type="text" class="form-control" name="bus_number" 
                                           placeholder="RD-005" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Modèle/Marque *</label>
                                    <input type="text" class="form-control" name="bus_model" 
                                           placeholder="Mercedes Sprinter" required>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nombre de Places *</label>
                                    <input type="number" class="form-control" name="total_seats" 
                                           min="10" max="70" placeholder="50" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Année</label>
                                    <input type="number" class="form-control" name="year" 
                                           min="2000" max="2025" placeholder="2023">
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Statut *</label>
                                    <select class="form-select" name="status" required>
                                        <option value="disponible">Disponible</option>
                                        <option value="en_route">En Route</option>
                                        <option value="maintenance">En Maintenance</option>
                                        <option value="hors_service">Hors Service</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Kilométrage</label>
                                    <input type="number" class="form-control" name="mileage" 
                                           placeholder="150000">
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Notes (optionnel)</label>
                                <textarea class="form-control" name="notes" rows="2" 
                                          placeholder="Informations supplémentaires..."></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Annuler
                        </button>
                        <button type="button" class="btn btn-success" onclick="saveBus()">
                            <i class="fas fa-save"></i> Ajouter le Bus
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Modal Nouveau Voyage -->
        <div class="modal fade" id="addTripModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-plus"></i> Programmer un Nouveau Voyage
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addTripForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Ville de Départ *</label>
                                    <select class="form-select" name="departure_city" required>
                                        <option value="">Sélectionner...</option>
                                        <option value="Yaoundé">Yaoundé</option>
                                        <option value="Douala">Douala</option>
                                        <option value="Bafoussam">Bafoussam</option>
                                        <option value="Bamenda">Bamenda</option>
                                        <option value="Garoua">Garoua</option>
                                        <option value="Maroua">Maroua</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Ville d'Arrivée *</label>
                                    <select class="form-select" name="arrival_city" required>
                                        <option value="">Sélectionner...</option>
                                        <option value="Yaoundé">Yaoundé</option>
                                        <option value="Douala">Douala</option>
                                        <option value="Bafoussam">Bafoussam</option>
                                        <option value="Bamenda">Bamenda</option>
                                        <option value="Garoua">Garoua</option>
                                        <option value="Maroua">Maroua</option>
                                        <option value="Kribi">Kribi</option>
                                        <option value="Bertoua">Bertoua</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Date *</label>
                                    <input type="date" class="form-control" name="date" required>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Heure de Départ *</label>
                                    <input type="time" class="form-control" name="departure_time" required>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Durée Estimée</label>
                                    <input type="text" class="form-control" name="duration" placeholder="Ex: 4h30">
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Bus Assigné *</label>
                                    <select class="form-select" name="bus_id" required>
                                        <option value="">Sélectionner un bus...</option>
                                        <option value="RD-001">RD-001 (50 places) - Disponible</option>
                                        <option value="RD-002">RD-002 (45 places) - Disponible</option>
                                        <option value="RD-003">RD-003 (55 places) - Disponible</option>
                                        <option value="RD-004">RD-004 (40 places) - Disponible</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Places Disponibles</label>
                                    <input type="number" class="form-control" name="available_seats" min="1" max="60" value="50">
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Prix Aller Simple (XAF) *</label>
                                    <input type="number" class="form-control" name="price_simple" min="1000" step="100" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Prix Aller-Retour (XAF) *</label>
                                    <input type="number" class="form-control" name="price_return" min="1500" step="100" required>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Notes (optionnel)</label>
                                <textarea class="form-control" name="notes" rows="2" placeholder="Informations supplémentaires..."></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Annuler
                        </button>
                        <button type="button" class="btn btn-success" onclick="saveTrip()">
                            <i class="fas fa-save"></i> Programmer le Voyage
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            class AdminManager {
                constructor() {
                    this.trips = JSON.parse(localStorage.getItem('trips') || '[]');
                    this.bookings = JSON.parse(localStorage.getItem('bookings') || '[]');
                    this.buses = JSON.parse(localStorage.getItem('buses') || this.getDefaultBuses());
                    this.init();
                }

                getDefaultBuses() {
                    return [
                        {
                            id: 1,
                            bus_number: 'RD-001',
                            bus_model: 'Mercedes Sprinter',
                            total_seats: 50,
                            year: 2023,
                            status: 'disponible',
                            mileage: 25000,
                            notes: 'Bus principal pour les longs trajets'
                        },
                        {
                            id: 2,
                            bus_number: 'RD-002',
                            bus_model: 'Iveco Daily',
                            total_seats: 45,
                            year: 2022,
                            status: 'disponible',
                            mileage: 18000,
                            notes: 'Bus de luxe avec climatisation'
                        },
                        {
                            id: 3,
                            bus_number: 'RD-003',
                            bus_model: 'Toyota Hiace',
                            total_seats: 25,
                            year: 2021,
                            status: 'maintenance',
                            mileage: 45000,
                            notes: 'Entretien programmé'
                        }
                    ];
                }

                init() {
                    this.checkAuth();
                    this.loadDashboard();
                    this.loadTrips();
                    this.loadBookings();
                    this.loadBuses();
                    
                    // Initialiser les dates par défaut pour les rapports
                    const today = new Date();
                    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
                    
                    const startInput = document.getElementById('reportStartDate');
                    const endInput = document.getElementById('reportEndDate');
                    
                    if (startInput) startInput.value = firstDay.toISOString().split('T')[0];
                    if (endInput) endInput.value = today.toISOString().split('T')[0];
                    
                    // Générer le rapport initial
                    setTimeout(() => this.generateFinancialReport(), 500);
                }

                checkAuth() {
                    const user = JSON.parse(localStorage.getItem('userInfo') || 'null');
                    if (!user || user.role !== 'admin') {
                        window.location.href = '/login/';
                        return;
                    }
                    document.getElementById('adminName').textContent = user.first_name + ' ' + user.last_name;
                }

                loadDashboard() {
                    document.getElementById('totalTrips').textContent = this.trips.length;
                    document.getElementById('totalBookings').textContent = this.bookings.filter(b => b.status !== 'cancelled' && b.status !== 'refunded').length;
                    
                    // Calculer les revenus réels (confirmées + validées seulement)
                    const activeBookings = this.bookings.filter(b => b.status === 'confirmed' || b.status === 'validated');
                    const totalRevenue = activeBookings.reduce((sum, booking) => sum + booking.total_price, 0);
                    document.getElementById('totalRevenue').textContent = totalRevenue.toLocaleString();
                    
                    // Mettre à jour le nombre de bus disponibles
                    const availableBuses = this.buses.filter(bus => bus.status === 'disponible').length;
                    const busCountElement = document.querySelector('.col-md-3:nth-child(2) h3');
                    if (busCountElement) {
                        busCountElement.textContent = availableBuses;
                    }
                }

                loadTrips() {
                    const tableBody = document.getElementById('tripsTable');
                    if (!tableBody) return;
                    
                    if (this.trips.length === 0) {
                        tableBody.innerHTML = '<tr><td colspan="9" class="text-center">Aucun voyage programmé</td></tr>';
                        return;
                    }
                    
                    const tripsHtml = this.trips.map((trip, index) => `
                        <tr>
                            <td>#${trip.id || index + 1}</td>
                            <td>${new Date(trip.date).toLocaleDateString('fr-FR')}</td>
                            <td>${trip.departure_city} → ${trip.arrival_city}</td>
                            <td>${trip.departure_time}${trip.duration ? ' (' + trip.duration + ')' : ''}</td>
                            <td>${trip.bus_id}</td>
                            <td>${trip.price_simple.toLocaleString()} / ${trip.price_return.toLocaleString()} XAF</td>
                            <td>${trip.available_seats}</td>
                            <td><span class="badge bg-success">Actif</span></td>
                            <td>
                                <button class="btn btn-sm btn-primary me-1" onclick="editTrip(${index})">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="deleteTrip(${index})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                    
                    tableBody.innerHTML = tripsHtml;
                }

                loadBookings() {
                    const tableBody = document.getElementById('bookingsTable');
                    if (!tableBody) return;
                    
                    if (this.bookings.length === 0) {
                        tableBody.innerHTML = '<tr><td colspan="8" class="text-center">Aucune réservation</td></tr>';
                        this.updateBookingStats();
                        return;
                    }
                    
                    const bookingsHtml = this.bookings.map((booking, index) => {
                        const statusBadge = this.getBookingStatusBadge(booking.status);
                        const actionButtons = this.getBookingActionButtons(booking, index);
                        
                        return `
                            <tr class="${booking.status === 'cancelled' ? 'table-secondary' : ''}">
                                <td><strong>${booking.ticket_number}</strong></td>
                                <td>
                                    ${booking.client_name}<br>
                                    <small class="text-muted">${booking.client_email}</small>
                                </td>
                                <td>
                                    ${booking.route}<br>
                                    <small class="text-muted">Bus ${booking.bus_id}</small>
                                </td>
                                <td>
                                    ${new Date(booking.date).toLocaleDateString('fr-FR')}<br>
                                    <small class="text-muted">${booking.departure_time}</small>
                                </td>
                                <td>
                                    <span class="badge bg-info">${booking.seats} place${booking.seats > 1 ? 's' : ''}</span><br>
                                    <small class="text-muted">${booking.trip_type === 'retour' ? 'Aller-Retour' : 'Aller Simple'}</small>
                                </td>
                                <td>
                                    <strong>${booking.total_price.toLocaleString()} XAF</strong><br>
                                    <small class="text-success">Stripe</small>
                                </td>
                                <td>${statusBadge}</td>
                                <td>${actionButtons}</td>
                            </tr>
                        `;
                    }).join('');
                    
                    tableBody.innerHTML = bookingsHtml;
                    this.updateBookingStats();
                }

                getBookingStatusBadge(status) {
                    const badges = {
                        'confirmed': '<span class="badge bg-success">Confirmée</span>',
                        'validated': '<span class="badge bg-primary">Validée</span>',
                        'cancelled': '<span class="badge bg-secondary">Annulée</span>',
                        'refunded': '<span class="badge bg-warning">Remboursée</span>'
                    };
                    return badges[status] || '<span class="badge bg-light">Inconnu</span>';
                }

                getBookingActionButtons(booking, index) {
                    if (booking.status === 'confirmed') {
                        return `
                            <div class="btn-group-vertical btn-group-sm">
                                <button class="btn btn-success btn-sm" onclick="validateTicket(${index})" title="Valider l'embarquement">
                                    <i class="fas fa-check"></i> Valider
                                </button>
                                <button class="btn btn-warning btn-sm" onclick="cancelBooking(${index})" title="Annuler/Rembourser">
                                    <i class="fas fa-times"></i> Annuler
                                </button>
                            </div>
                        `;
                    } else if (booking.status === 'validated') {
                        return `
                            <div class="btn-group-vertical btn-group-sm">
                                <button class="btn btn-outline-success btn-sm" disabled>
                                    <i class="fas fa-check-circle"></i> Embarqué
                                </button>
                                <button class="btn btn-info btn-sm" onclick="viewBookingDetails(${index})">
                                    <i class="fas fa-eye"></i> Détails
                                </button>
                            </div>
                        `;
                    } else {
                        return `
                            <button class="btn btn-outline-secondary btn-sm" onclick="viewBookingDetails(${index})">
                                <i class="fas fa-eye"></i> Voir
                            </button>
                        `;
                    }
                }

                updateBookingStats() {
                    const confirmed = this.bookings.filter(b => b.status === 'confirmed').length;
                    const validated = this.bookings.filter(b => b.status === 'validated').length;
                    const cancelled = this.bookings.filter(b => b.status === 'cancelled' || b.status === 'refunded').length;
                    
                    const confirmedElement = document.getElementById('confirmedCount');
                    const validatedElement = document.getElementById('validatedCount');
                    const cancelledElement = document.getElementById('cancelledCount');
                    
                    if (confirmedElement) confirmedElement.textContent = `${confirmed} Confirmées`;
                    if (validatedElement) validatedElement.textContent = `${validated} Validées`;
                    if (cancelledElement) cancelledElement.textContent = `${cancelled} Annulées`;
                }

                loadBuses() {
                    // Charger la grille des bus
                    const busesGrid = document.getElementById('busesGrid');
                    if (busesGrid) {
                        const busCards = this.buses.map(bus => this.createBusCard(bus)).join('');
                        busesGrid.innerHTML = busCards;
                    }
                    
                    // Charger le tableau des bus
                    const busesTable = document.getElementById('busesTable');
                    if (busesTable) {
                        if (this.buses.length === 0) {
                            busesTable.innerHTML = '<tr><td colspan="6" class="text-center">Aucun bus enregistré</td></tr>';
                            return;
                        }
                        
                        const busRows = this.buses.map((bus, index) => `
                            <tr>
                                <td><strong>${bus.bus_number}</strong></td>
                                <td>${bus.bus_model}</td>
                                <td>${bus.total_seats} places</td>
                                <td>${this.getBusStatusBadge(bus.status)}</td>
                                <td>${bus.last_maintenance || 'N/A'}</td>
                                <td>
                                    <button class="btn btn-sm btn-primary me-1" onclick="editBus(${index})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="btn btn-sm btn-danger" onclick="deleteBus(${index})">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('');
                        
                        busesTable.innerHTML = busRows;
                    }
                    
                    // Mettre à jour les options de bus dans le formulaire de voyage
                    this.updateBusOptions();
                }

                generateFinancialReport(startDate = null, endDate = null) {
                    const today = new Date();
                    const defaultStart = new Date(today.getFullYear(), today.getMonth(), 1); // Début du mois
                    const defaultEnd = today;
                    
                    const start = startDate || defaultStart;
                    const end = endDate || defaultEnd;
                    
                    // Filtrer les réservations par période
                    const filteredBookings = this.bookings.filter(booking => {
                        const bookingDate = new Date(booking.booking_date);
                        return bookingDate >= start && bookingDate <= end;
                    });
                    
                    // Calculer les métriques
                    const confirmedBookings = filteredBookings.filter(b => b.status === 'confirmed' || b.status === 'validated');
                    const refundedBookings = filteredBookings.filter(b => b.status === 'refunded');
                    
                    const totalRevenue = confirmedBookings.reduce((sum, b) => sum + b.total_price, 0);
                    const totalRefunds = refundedBookings.reduce((sum, b) => sum + b.total_price, 0);
                    const netRevenue = totalRevenue - totalRefunds;
                    const totalTickets = confirmedBookings.reduce((sum, b) => sum + b.seats, 0);
                    
                    // Mettre à jour l'affichage
                    document.getElementById('totalRevenueReport').textContent = totalRevenue.toLocaleString();
                    document.getElementById('totalTicketsSold').textContent = totalTickets;
                    document.getElementById('totalRefunds').textContent = totalRefunds.toLocaleString();
                    document.getElementById('netRevenue').textContent = netRevenue.toLocaleString();
                    
                    // Répartition par statut
                    this.updateStatusBreakdown(filteredBookings);
                    
                    // Top routes
                    this.updateTopRoutes(filteredBookings);
                    
                    // Tableau des transactions
                    this.updateTransactionsTable(filteredBookings);
                }

                updateStatusBreakdown(bookings) {
                    const statusCounts = {
                        confirmed: { count: 0, revenue: 0 },
                        validated: { count: 0, revenue: 0 },
                        refunded: { count: 0, revenue: 0 },
                        cancelled: { count: 0, revenue: 0 }
                    };
                    
                    bookings.forEach(booking => {
                        if (statusCounts[booking.status]) {
                            statusCounts[booking.status].count++;
                            statusCounts[booking.status].revenue += booking.total_price;
                        }
                    });
                    
                    const breakdownHtml = Object.entries(statusCounts).map(([status, data]) => {
                        const statusLabels = {
                            confirmed: 'Confirmées',
                            validated: 'Validées',
                            refunded: 'Remboursées',
                            cancelled: 'Annulées'
                        };
                        
                        const statusColors = {
                            confirmed: 'success',
                            validated: 'primary',
                            refunded: 'warning',
                            cancelled: 'secondary'
                        };
                        
                        return `
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="badge bg-${statusColors[status]}">${statusLabels[status]}</span>
                                <div class="text-end">
                                    <div><strong>${data.count} tickets</strong></div>
                                    <small class="text-muted">${data.revenue.toLocaleString()} XAF</small>
                                </div>
                            </div>
                        `;
                    }).join('');
                    
                    document.getElementById('statusBreakdown').innerHTML = breakdownHtml;
                }

                updateTopRoutes(bookings) {
                    const routeStats = {};
                    
                    bookings.filter(b => b.status === 'confirmed' || b.status === 'validated').forEach(booking => {
                        if (!routeStats[booking.route]) {
                            routeStats[booking.route] = { tickets: 0, revenue: 0 };
                        }
                        routeStats[booking.route].tickets += booking.seats;
                        routeStats[booking.route].revenue += booking.total_price;
                    });
                    
                    const sortedRoutes = Object.entries(routeStats)
                        .sort(([,a], [,b]) => b.revenue - a.revenue)
                        .slice(0, 5);
                    
                    const routesHtml = sortedRoutes.map(([route, stats], index) => `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span><strong>${index + 1}. ${route}</strong></span>
                            <div class="text-end">
                                <div><strong>${stats.revenue.toLocaleString()} XAF</strong></div>
                                <small class="text-muted">${stats.tickets} places</small>
                            </div>
                        </div>
                    `).join('');
                    
                    document.getElementById('topRoutes').innerHTML = routesHtml || '<p class="text-muted">Aucune donnée disponible</p>';
                }

                updateTransactionsTable(bookings) {
                    const tableBody = document.getElementById('transactionsTable');
                    
                    if (bookings.length === 0) {
                        tableBody.innerHTML = '<tr><td colspan="8" class="text-center">Aucune transaction pour cette période</td></tr>';
                        return;
                    }
                    
                    const transactionsHtml = bookings.map(booking => {
                        const impactClass = booking.status === 'refunded' ? 'text-danger' : 'text-success';
                        const impactSign = booking.status === 'refunded' ? '-' : '+';
                        
                        return `
                            <tr class="${booking.status === 'refunded' ? 'table-warning' : ''}">
                                <td>${new Date(booking.booking_date).toLocaleDateString('fr-FR')}</td>
                                <td><strong>${booking.ticket_number}</strong></td>
                                <td>${booking.client_name}</td>
                                <td>${booking.route}</td>
                                <td>${booking.seats}</td>
                                <td>${booking.total_price.toLocaleString()} XAF</td>
                                <td>${this.getBookingStatusBadge(booking.status)}</td>
                                <td class="${impactClass}">
                                    <strong>${impactSign}${booking.total_price.toLocaleString()} XAF</strong>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    
                    tableBody.innerHTML = transactionsHtml;
                }

                createBusCard(bus) {
                    const statusClass = {
                        'disponible': 'success',
                        'en_route': 'warning', 
                        'maintenance': 'danger',
                        'hors_service': 'secondary'
                    };
                    
                    return `
                        <div class="col-md-4 mb-3">
                            <div class="card border-${statusClass[bus.status]}">
                                <div class="card-body">
                                    <h6 class="card-title">
                                        <i class="fas fa-bus"></i> ${bus.bus_number}
                                    </h6>
                                    <p class="card-text">
                                        <strong>Modèle:</strong> ${bus.bus_model}<br>
                                        <strong>Places:</strong> ${bus.total_seats}<br>
                                        <strong>Année:</strong> ${bus.year || 'N/A'}
                                    </p>
                                    ${this.getBusStatusBadge(bus.status)}
                                    <div class="mt-2">
                                        <small class="text-muted">
                                            ${bus.mileage ? bus.mileage.toLocaleString() + ' km' : 'N/A'}
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                getBusStatusBadge(status) {
                    const badges = {
                        'disponible': '<span class="badge bg-success">Disponible</span>',
                        'en_route': '<span class="badge bg-warning">En Route</span>',
                        'maintenance': '<span class="badge bg-danger">Maintenance</span>',
                        'hors_service': '<span class="badge bg-secondary">Hors Service</span>'
                    };
                    return badges[status] || '<span class="badge bg-light">Inconnu</span>';
                }

                updateBusOptions() {
                    const busSelect = document.querySelector('select[name="bus_id"]');
                    if (busSelect) {
                        const availableBuses = this.buses.filter(bus => bus.status === 'disponible');
                        const options = availableBuses.map(bus => 
                            `<option value="${bus.bus_number}">${bus.bus_number} (${bus.total_seats} places) - ${bus.bus_model}</option>`
                        ).join('');
                        
                        busSelect.innerHTML = '<option value="">Sélectionner un bus...</option>' + options;
                    }
                }
            }

            // Fonctions globales
            function showSection(sectionName) {
                document.querySelectorAll('.content-section').forEach(section => {
                    section.style.display = 'none';
                });
                document.getElementById(sectionName + '-section').style.display = 'block';
                
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                event.target.classList.add('active');
            }

            function showAddTripModal() {
                document.querySelector('input[name="date"]').min = new Date().toISOString().split('T')[0];
                new bootstrap.Modal(document.getElementById('addTripModal')).show();
            }

            function showAddBusModal() {
                new bootstrap.Modal(document.getElementById('addBusModal')).show();
            }

            function saveBus() {
                const form = document.getElementById('addBusForm');
                const formData = new FormData(form);
                
                if (!form.checkValidity()) {
                    form.classList.add('was-validated');
                    return;
                }
                
                // Vérifier si le numéro de bus existe déjà
                const busNumber = formData.get('bus_number');
                const existingBus = adminManager.buses.find(bus => bus.bus_number === busNumber);
                if (existingBus) {
                    alert('Un bus avec ce numéro existe déjà !');
                    return;
                }
                
                const busData = {
                    id: Date.now(),
                    bus_number: busNumber,
                    bus_model: formData.get('bus_model'),
                    total_seats: parseInt(formData.get('total_seats')),
                    year: parseInt(formData.get('year')) || null,
                    status: formData.get('status'),
                    mileage: parseInt(formData.get('mileage')) || 0,
                    notes: formData.get('notes') || '',
                    created_at: new Date().toISOString()
                };
                
                adminManager.buses.push(busData);
                localStorage.setItem('buses', JSON.stringify(adminManager.buses));
                
                adminManager.loadBuses();
                adminManager.loadDashboard();
                
                bootstrap.Modal.getInstance(document.getElementById('addBusModal')).hide();
                form.reset();
                form.classList.remove('was-validated');
                
                alert('Bus ajouté avec succès !');
            }

            function deleteBus(index) {
                const bus = adminManager.buses[index];
                if (confirm(`Êtes-vous sûr de vouloir supprimer le bus ${bus.bus_number} ?`)) {
                    adminManager.buses.splice(index, 1);
                    localStorage.setItem('buses', JSON.stringify(adminManager.buses));
                    adminManager.loadBuses();
                    adminManager.loadDashboard();
                }
            }

            function showTicketValidationModal() {
                document.getElementById('ticketNumberInput').value = '';
                document.getElementById('ticketSearchResult').innerHTML = '';
                new bootstrap.Modal(document.getElementById('ticketValidationModal')).show();
            }

            function searchTicketByNumber() {
                const ticketNumber = document.getElementById('ticketNumberInput').value.trim();
                const resultDiv = document.getElementById('ticketSearchResult');
                
                if (ticketNumber.length < 3) {
                    resultDiv.innerHTML = '';
                    return;
                }
                
                const booking = adminManager.bookings.find(b => 
                    b.ticket_number.toLowerCase().includes(ticketNumber.toLowerCase())
                );
                
                if (booking) {
                    const statusColor = {
                        'confirmed': 'success',
                        'validated': 'primary', 
                        'cancelled': 'secondary',
                        'refunded': 'warning'
                    };
                    
                    resultDiv.innerHTML = `
                        <div class="card border-${statusColor[booking.status]}">
                            <div class="card-header bg-${statusColor[booking.status]} text-white">
                                <h6 class="mb-0">Ticket Trouvé: ${booking.ticket_number}</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-6">
                                        <strong>Client:</strong> ${booking.client_name}<br>
                                        <strong>Email:</strong> ${booking.client_email}<br>
                                        <strong>Route:</strong> ${booking.route}
                                    </div>
                                    <div class="col-6">
                                        <strong>Date:</strong> ${new Date(booking.date).toLocaleDateString('fr-FR')}<br>
                                        <strong>Heure:</strong> ${booking.departure_time}<br>
                                        <strong>Places:</strong> ${booking.seats}
                                    </div>
                                </div>
                                <div class="mt-3">
                                    <strong>Statut:</strong> ${adminManager.getBookingStatusBadge(booking.status)}
                                </div>
                                ${booking.status === 'confirmed' ? `
                                    <div class="mt-3 d-flex gap-2">
                                        <button class="btn btn-success btn-sm" onclick="validateTicketFromModal('${booking.ticket_number}')">
                                            <i class="fas fa-check"></i> Valider Embarquement
                                        </button>
                                        <button class="btn btn-warning btn-sm" onclick="cancelBookingFromModal('${booking.ticket_number}')">
                                            <i class="fas fa-times"></i> Annuler/Rembourser
                                        </button>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            Aucun ticket trouvé avec ce numéro.
                        </div>
                    `;
                }
            }

            function validateTicket(index) {
                const booking = adminManager.bookings[index];
                showConfirmationModal(
                    'Valider le Ticket',
                    `
                        <p>Confirmer l'embarquement pour :</p>
                        <ul>
                            <li><strong>Ticket:</strong> ${booking.ticket_number}</li>
                            <li><strong>Client:</strong> ${booking.client_name}</li>
                            <li><strong>Voyage:</strong> ${booking.route}</li>
                            <li><strong>Places:</strong> ${booking.seats}</li>
                        </ul>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            Le client recevra un email de confirmation d'embarquement.
                        </div>
                    `,
                    'btn-success',
                    () => performTicketValidation(index)
                );
            }

            function cancelBooking(index) {
                const booking = adminManager.bookings[index];
                showConfirmationModal(
                    'Annuler et Rembourser',
                    `
                        <p>Annuler la réservation et rembourser :</p>
                        <ul>
                            <li><strong>Ticket:</strong> ${booking.ticket_number}</li>
                            <li><strong>Client:</strong> ${booking.client_name}</li>
                            <li><strong>Montant:</strong> ${booking.total_price.toLocaleString()} XAF</li>
                        </ul>
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            Cette action annulera la réservation et initiera le remboursement.
                        </div>
                    `,
                    'btn-warning',
                    () => performBookingCancellation(index)
                );
            }

            function showConfirmationModal(title, content, buttonClass, callback) {
                document.getElementById('confirmActionTitle').textContent = title;
                document.getElementById('confirmActionContent').innerHTML = content;
                document.getElementById('emailNotificationSection').style.display = 'block';
                
                const confirmButton = document.getElementById('confirmActionButton');
                confirmButton.className = `btn ${buttonClass}`;
                confirmButton.textContent = 'Confirmer';
                confirmButton.onclick = callback;
                
                new bootstrap.Modal(document.getElementById('confirmActionModal')).show();
            }

            function performTicketValidation(index) {
                const booking = adminManager.bookings[index];
                const sendEmail = document.getElementById('sendEmailConfirmation').checked;
                
                // Mettre à jour le statut
                booking.status = 'validated';
                booking.validated_at = new Date().toISOString();
                booking.validated_by = JSON.parse(localStorage.getItem('userInfo')).username;
                
                // Sauvegarder
                localStorage.setItem('bookings', JSON.stringify(adminManager.bookings));
                
                // Simuler l'envoi d'email
                if (sendEmail) {
                    setTimeout(() => {
                        alert(`Email de confirmation d'embarquement envoyé à ${booking.client_email}`);
                    }, 1000);
                }
                
                // Actualiser l'affichage
                adminManager.loadBookings();
                adminManager.loadDashboard(); // Mettre à jour les revenus
                bootstrap.Modal.getInstance(document.getElementById('confirmActionModal')).hide();
                
                alert('Ticket validé avec succès !');
                
                // Mettre à jour les rapports financiers si visibles
                if (document.getElementById('payments-section').style.display !== 'none') {
                    adminManager.generateFinancialReport();
                }
            }

            function performBookingCancellation(index) {
                const booking = adminManager.bookings[index];
                const sendEmail = document.getElementById('sendEmailConfirmation').checked;
                
                // Mettre à jour le statut
                booking.status = 'refunded';
                booking.cancelled_at = new Date().toISOString();
                booking.cancelled_by = JSON.parse(localStorage.getItem('userInfo')).username;
                
                // Sauvegarder
                localStorage.setItem('bookings', JSON.stringify(adminManager.bookings));
                
                // Simuler l'envoi d'email de remboursement
                if (sendEmail) {
                    setTimeout(() => {
                        alert(`Email de confirmation de remboursement envoyé à ${booking.client_email}`);
                    }, 1000);
                }
                
                // Actualiser l'affichage
                adminManager.loadBookings();
                bootstrap.Modal.getInstance(document.getElementById('confirmActionModal')).hide();
                
                alert('Réservation annulée et remboursement initié !');
                
                // Mettre à jour les rapports financiers
                if (document.getElementById('payments-section').style.display !== 'none') {
                    adminManager.generateFinancialReport();
                }
            }

            function generateFinancialReport() {
                const startDate = document.getElementById('reportStartDate').value;
                const endDate = document.getElementById('reportEndDate').value;
                
                const start = startDate ? new Date(startDate) : null;
                const end = endDate ? new Date(endDate) : null;
                
                adminManager.generateFinancialReport(start, end);
            }

            function updateFinancialReport() {
                generateFinancialReport();
            }

            function setPredefinedPeriod() {
                const period = document.getElementById('predefinedPeriod').value;
                const today = new Date();
                let startDate, endDate;
                
                switch (period) {
                    case 'today':
                        startDate = endDate = today;
                        break;
                    case 'week':
                        startDate = new Date(today.setDate(today.getDate() - today.getDay()));
                        endDate = new Date();
                        break;
                    case 'month':
                        startDate = new Date(today.getFullYear(), today.getMonth(), 1);
                        endDate = new Date();
                        break;
                    case 'quarter':
                        const quarter = Math.floor(today.getMonth() / 3);
                        startDate = new Date(today.getFullYear(), quarter * 3, 1);
                        endDate = new Date();
                        break;
                    case 'year':
                        startDate = new Date(today.getFullYear(), 0, 1);
                        endDate = new Date();
                        break;
                    default:
                        return;
                }
                
                document.getElementById('reportStartDate').value = startDate.toISOString().split('T')[0];
                document.getElementById('reportEndDate').value = endDate.toISOString().split('T')[0];
                
                generateFinancialReport();
            }

            function validateTicketFromModal(ticketNumber) {
                const index = adminManager.bookings.findIndex(b => b.ticket_number === ticketNumber);
                if (index !== -1) {
                    bootstrap.Modal.getInstance(document.getElementById('ticketValidationModal')).hide();
                    validateTicket(index);
                }
            }

            function cancelBookingFromModal(ticketNumber) {
                const index = adminManager.bookings.findIndex(b => b.ticket_number === ticketNumber);
                if (index !== -1) {
                    bootstrap.Modal.getInstance(document.getElementById('ticketValidationModal')).hide();
                    cancelBooking(index);
                }
            }

            function saveTrip() {
                const form = document.getElementById('addTripForm');
                const formData = new FormData(form);
                
                if (!form.checkValidity()) {
                    form.classList.add('was-validated');
                    return;
                }
                
                const tripData = {
                    id: Date.now(),
                    departure_city: formData.get('departure_city'),
                    arrival_city: formData.get('arrival_city'),
                    date: formData.get('date'),
                    departure_time: formData.get('departure_time'),
                    duration: formData.get('duration'),
                    bus_id: formData.get('bus_id'),
                    available_seats: parseInt(formData.get('available_seats')),
                    price_simple: parseInt(formData.get('price_simple')),
                    price_return: parseInt(formData.get('price_return')),
                    notes: formData.get('notes'),
                    created_at: new Date().toISOString()
                };
                
                adminManager.trips.push(tripData);
                localStorage.setItem('trips', JSON.stringify(adminManager.trips));
                
                adminManager.loadTrips();
                adminManager.loadDashboard();
                
                bootstrap.Modal.getInstance(document.getElementById('addTripModal')).hide();
                form.reset();
                form.classList.remove('was-validated');
                
                alert('Voyage programmé avec succès !');
            }

            function deleteTrip(index) {
                if (confirm('Êtes-vous sûr de vouloir supprimer ce voyage ?')) {
                    adminManager.trips.splice(index, 1);
                    localStorage.setItem('trips', JSON.stringify(adminManager.trips));
                    adminManager.loadTrips();
                    adminManager.loadDashboard();
                }
            }

            function logout() {
                if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('userInfo');
                    window.location.href = '/';
                }
            }

            // Initialiser
            let adminManager;
            document.addEventListener('DOMContentLoaded', () => {
                adminManager = new AdminManager();
            });
        </script>
    </body>
    </html>
    """, content_type='text/html')

# APIs simples
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        # Comptes de test
        test_accounts = {
            'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Administrateur Principal'},
            'manager': {'password': 'manager123', 'role': 'admin', 'name': 'Manager Transport'},
            'client1': {'password': 'client123', 'role': 'client', 'name': 'Jean Dupont'},
            'marie': {'password': 'marie123', 'role': 'client', 'name': 'Marie Ngono'},
            'paul': {'password': 'paul123', 'role': 'client', 'name': 'Paul Mbassa'},
        }
        
        if username in test_accounts and test_accounts[username]['password'] == password:
            # Extraire le prénom et nom à partir du nom complet
            name_parts = test_accounts[username]['name'].split()
            first_name = name_parts[0] if len(name_parts) > 0 else username
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            return JsonResponse({
                'status': 'success',
                'token': f'token_{username}',
                'user': {
                    'username': username,
                    'role': test_accounts[username]['role'],
                    'first_name': first_name,
                    'last_name': last_name,
                    'full_name': test_accounts[username]['name']
                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Nom d\'utilisateur ou mot de passe incorrect'
            })
    
    return JsonResponse({'error': 'Méthode non autorisée'})

# URLs
urlpatterns = [
    path('login/', serve_login, name='login'),
    path('register/', serve_register, name='register'),
    path('client/', serve_client, name='client'),
    path('admin-backoffice/', serve_admin_backoffice, name='admin_backoffice'),
    
    # APIs
    path('api/auth/login/', api_login, name='api_login'),
]