# bookings/views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Route, Trip, Booking
from .serializers import RouteSerializer, TripSerializer, BookingSerializer

class RouteListView(generics.ListAPIView):
    queryset = Route.objects.filter(is_active=True)
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]

class TripSearchView(generics.ListAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Trip.objects.filter(status='scheduled')
        
        departure_city = self.request.query_params.get('departure_city')
        arrival_city = self.request.query_params.get('arrival_city')
        departure_date = self.request.query_params.get('departure_date')
        
        if departure_city:
            queryset = queryset.filter(route__departure_city__icontains=departure_city)
        if arrival_city:
            queryset = queryset.filter(route__arrival_city__icontains=arrival_city)
        if departure_date:
            date_obj = datetime.strptime(departure_date, '%Y-%m-%d').date()
            queryset = queryset.filter(departure_time__date=date_obj)
        
        return queryset.order_by('departure_time')

@api_view(['POST'])
def create_booking(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save(client=request.user)
        return Response({
            'booking': BookingSerializer(booking).data,
            'message': 'Réservation créée avec succès'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def my_bookings(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    bookings = Booking.objects.filter(client=request.user).order_by('-booking_date')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

class BookingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user)