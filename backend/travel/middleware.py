# travel/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware qui force l'authentification sur toutes les pages
    sauf celles explicitement exemptées
    """
    
    def process_request(self, request):
        # URLs qui ne nécessitent pas d'authentification
        exempt_urls = [
            '/auth/login/',
            '/auth/logout/',
            '/admin/',
            '/api/',
        ]
        
        # Si l'utilisateur n'est pas authentifié
        if not request.user.is_authenticated:
            # Vérifier si l'URL actuelle nécessite une authentification
            path = request.path_info
            
            # Si ce n'est pas une URL exemptée, rediriger vers login
            if not any(path.startswith(url) for url in exempt_urls):
                return redirect('/auth/login/')
        
        return None
  