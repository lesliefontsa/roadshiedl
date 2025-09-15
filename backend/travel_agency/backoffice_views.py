from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import FileResponse, Http404
from django.conf import settings
import os

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_staff)(view_func)

def serve_static_file(request, filename):
    """Servir les fichiers HTML à la racine du projet"""
    file_path = os.path.join(settings.BASE_DIR.parent, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    raise Http404("File not found")

@staff_required
def admin_backoffice(request):
    return render(request, 'admin-backoffice.html')

@staff_required
def admin_backoffice_fixed(request):
    return render(request, 'admin-backoffice-fixed.html')
