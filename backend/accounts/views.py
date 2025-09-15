# accounts/views.py
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserSerializer, ClientProfileSerializer, DriverProfileSerializer
)
from .authentication import generate_jwt_token
from .models import ClientProfile, DriverProfile

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = generate_jwt_token(user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token,
            'message': 'Inscription réussie'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = generate_jwt_token(user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token,
            'message': 'Connexion réussie'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile(request):
    user = request.user
    data = UserSerializer(user).data
    
    if user.role == 'client' and hasattr(user, 'client_profile'):
        data['profile'] = ClientProfileSerializer(user.client_profile).data
    elif user.role == 'driver' and hasattr(user, 'driver_profile'):
        data['profile'] = DriverProfileSerializer(user.driver_profile).data
    
    return Response(data)

@api_view(['PUT'])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'Profil mis à jour'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return User.objects.all()
        return User.objects.filter(id=user.id)