# alerts/views.py
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Alert, DriverBehaviorLog
from .serializers import AlertSerializer, DriverBehaviorLogSerializer

class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Alert.objects.all().order_by('-timestamp')
        
        # Filter by severity if provided
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by status if provided
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by time range
        hours = self.request.query_params.get('hours', 24)
        try:
            hours = int(hours)
            since = timezone.now() - timedelta(hours=hours)
            queryset = queryset.filter(timestamp__gte=since)
        except ValueError:
            pass
        
        return queryset

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def acknowledge_alert(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.status = 'acknowledged'
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        return Response({
            'message': 'Alert acknowledged',
            'alert': AlertSerializer(alert).data
        })
    except Alert.DoesNotExist:
        return Response({'error': 'Alert not found'}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    # Get statistics for the dashboard
    now = timezone.now()
    today = now.date()
    
    stats = {
        'alerts_today': Alert.objects.filter(timestamp__date=today).count(),
        'critical_alerts': Alert.objects.filter(
            severity='critical', 
            status__in=['new', 'acknowledged']
        ).count(),
        'active_vehicles': 24,  # Cette valeur devrait venir de la base de données
        'average_speed': 65,    # Calculé à partir des données de tracking
    }
    
    # Recent alerts
    recent_alerts = Alert.objects.order_by('-timestamp')[:10]
    stats['recent_alerts'] = AlertSerializer(recent_alerts, many=True).data
    
    return Response(stats)