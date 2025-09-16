# vehicles/views.py
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Vehicle, VehicleTracking
from .serializers import VehicleSerializer, VehicleTrackingSerializer

class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.filter(status='active')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicle_tracking(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        tracking_data = VehicleTracking.objects.filter(vehicle=vehicle).order_by('-timestamp')[:20]
        serializer = VehicleTrackingSerializer(tracking_data, many=True)
        return Response(serializer.data)
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle not found'}, status=404)

@csrf_exempt
@api_view(['POST'])
def create_bus(request):
    """API pour créer un nouveau bus"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Mapper les champs du formulaire aux champs du modèle
        vehicle_data = {
            'registration_number': data.get('bus_number', ''),
            'brand': 'Bus',  # Valeur par défaut
            'model': data.get('bus_model', ''),
            'year': int(data.get('year', 2023)),
            'vehicle_type': 'bus',
            'capacity': int(data.get('total_seats', 50)),
            'status': 'active',  # Toujours actif pour les nouveaux bus
            'has_ac': data.get('has_ac', False),
            'has_wifi': data.get('has_wifi', False),
            'has_entertainment': data.get('has_entertainment', False),
        }
        
        # Créer le bus
        serializer = VehicleSerializer(data=vehicle_data)
        if serializer.is_valid():
            bus = serializer.save()
            return Response({
                'success': True,
                'message': f'Bus {bus.registration_number} créé avec succès!',
                'bus': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def list_buses(request):
    """API pour lister tous les bus"""
    try:
        buses = Vehicle.objects.filter(vehicle_type='bus').order_by('-created_at')
        serializer = VehicleSerializer(buses, many=True)
        return Response({
            'success': True,
            'buses': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)