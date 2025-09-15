# Vue de test simple pour l'API des voyages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  
def test_trips_view(request):
    """Vue de test ultra-simple"""
    return JsonResponse({
        'status': 'success',
        'message': 'API de test fonctionne',
        'trips': []
    })