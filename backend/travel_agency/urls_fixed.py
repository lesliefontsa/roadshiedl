from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
import os
from datetime import datetime

def home_view(request):
    """Page d'accueil principale"""
    home_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RoadShield Travel Agency - Accueil</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                display: flex;
                align-items: center;
            }
            .card { 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-10">
                    <div class="card">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <h1 class="display-4 mb-3">
                                    <i class="fas fa-shield-alt text-primary"></i> 
                                    RoadShield Travel Agency
                                </h1>
                                <p class="lead">Système de Réservation de Voyages avec Orange Money</p>
                                                                <div class="badge bg-success fs-6">✅ Page de Login Directe</div>
                            </div>
                            
                            <div class="row g-4">
                                <div class="col-md-6">
                                    <div class="card h-100 border-primary">
                                        <div class="card-body text-center">
                                            <i class="fas fa-users fa-3x text-primary mb-3"></i>
                                            <h4>Interfaces Utilisateurs</h4>
                                            <div class="d-grid gap-2">
                                                <a href="/login/" class="btn btn-primary">
                                                    <i class="fas fa-sign-in-alt"></i> Connexion
                                                </a>
                                                <a href="/register/" class="btn btn-success">
                                                    <i class="fas fa-user-plus"></i> Créer un Compte
                                                </a>
                                                <a href="/client-fixed.html" class="btn btn-outline-primary">
                                                    <i class="fas fa-bus"></i> Réserver un Voyage
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="card h-100 border-warning">
                                        <div class="card-body text-center">
                                            <i class="fas fa-cogs fa-3x text-warning mb-3"></i>
                                            <h4>Administration</h4>
                                            <div class="d-grid gap-2">
                                                <a href="/admin-backoffice/" class="btn btn-warning">
                                                    <i class="fas fa-route"></i> Gestion des Voyages
                                                </a>
                                                <a href="/admin-dashboard/" class="btn btn-outline-warning">
                                                    <i class="fas fa-tachometer-alt"></i> Dashboard Temps Réel
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <div class="card border-info">
                                        <div class="card-body">
                                            <h5><i class="fas fa-user-shield"></i> Comptes Admin</h5>
                                            <ul class="list-unstyled">
                                                <li><code>admin</code> / <code>admin123</code></li>
                                                <li><code>manager</code> / <code>manager123</code></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="card border-success">
                                        <div class="card-body">
                                            <h5><i class="fas fa-users"></i> Comptes Clients</h5>
                                            <ul class="list-unstyled">
                                                <li><code>client1</code> / <code>client123</code></li>
                                                <li><code>marie</code> / <code>marie123</code></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(home_content, content_type='text/html')