from rest_framework import serializers
from .models import User, Seeker, Provider

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Make password write-only so it never gets returned in an API response
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'location', 'role']

    def create(self, validated_data):
        # Create the base user and hash the password
        user = User.objects.create_user(**validated_data)
        
        # Automatically create the corresponding profile based on the role
        if user.role == User.RoleChoices.SEEKER:
            Seeker.objects.create(user=user)
        elif user.role == User.RoleChoices.PROVIDER:
            Provider.objects.create(user=user)
            
        return user