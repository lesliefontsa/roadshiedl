# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ClientProfile, DriverProfile
from .authentication import generate_jwt_token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 
                 'last_name', 'phone_number', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Create profile based on role
        if user.role == 'client':
            ClientProfile.objects.create(user=user)
        elif user.role == 'driver':
            DriverProfile.objects.create(
                user=user,
                license_number='',
                license_expiry='2025-01-01',
                experience_years=0
            )
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Identifiants invalides')
            if not user.is_active:
                raise serializers.ValidationError('Compte désactivé')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Username et mot de passe requis')
        
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'role', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']

class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ClientProfile
        fields = '__all__'

class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DriverProfile
        fields = '__all__'