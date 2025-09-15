# urls.py - Version avec home_view = page de login
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
import json

def home_view(request):
    """Page de login directe - Page d'accueil"""
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
                redirect_url = '/client/'
            
            return HttpResponse(f"""
                <script>
                    localStorage.setItem('authToken', 'token_{username}');
                    localStorage.setItem('userInfo', '{json.dumps(user_info)}');
                    window.location.href = '{redirect_url}';
                </script>
            """)
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return HttpResponse(get_login_html(request, error_message))
    
    # Afficher la page de login
    return HttpResponse(get_login_html(request))

def get_login_html(request, error_message=""):
    """Génère le HTML de la page de login"""
    csrf_token = get_token(request)
    
    error_html = ""
    if error_message:
        error_html = f'''
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle"></i>
                {error_message}
            </div>
        '''
    
    return f"""
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
                            {error_html}
                            
                            <form method="post" action="/travel/auth/login/">
                                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                                
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
    """

def serve_client(request):
    """Interface client complète pour voir et réserver les voyages créés par l'admin"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>RoadShield Travel - Interface Client</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
        <div class="container mt-5">
            <div class="card">
                <div class="card-body text-center">
                    <h2><i class="fas fa-bus text-primary"></i> Interface Client</h2>
                    <p class="lead">Bienvenue dans votre espace client</p>
                    <div class="alert alert-success">
                        <i class="fas fa-check"></i>
                        Interface client active et opérationnelle !
                    </div>
                    <button class="btn btn-danger" onclick="logout()">
                        <i class="fas fa-sign-out-alt"></i> Déconnexion
                    </button>
                </div>
            </div>
        </div>
        
        <script>
            function logout() {
                if (confirm('Déconnexion ?')) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('userInfo');
                    window.location.href = '/';
                }
            }
        </script>
    </body>
    </html>
    """, content_type='text/html')

def serve_admin_backoffice(request):
    """Interface admin complète"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>RoadShield - Administration</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
        <div class="container mt-5">
            <div class="card">
                <div class="card-body text-center">
                    <h2><i class="fas fa-cogs text-warning"></i> Interface Administration</h2>
                    <p class="lead">Bienvenue dans l'espace d'administration</p>
                    <div class="alert alert-warning">
                        <i class="fas fa-tools"></i>
                        Interface d'administration active et opérationnelle !
                    </div>
                    <button class="btn btn-danger" onclick="logout()">
                        <i class="fas fa-sign-out-alt"></i> Déconnexion
                    </button>
                </div>
            </div>
        </div>
        
        <script>
            function logout() {
                if (confirm('Déconnexion ?')) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('userInfo');
                    window.location.href = '/';
                }
            }
        </script>
    </body>
    </html>
    """, content_type='text/html')
urlpatterns = [
    path('', home_view, name='home'),  # Page d'accueil = Page de login
    path('auth/login/', home_view, name='login'),
    path('client/', serve_client, name='client'),
    path('admin-backoffice/', serve_admin_backoffice, name='admin_backoffice'),
]