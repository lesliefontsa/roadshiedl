# vehicles/views.py
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
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