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
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'location']
        read_only_fields = ['id', 'username', 'email', 'role']    #making these read-only so a Seeker can't hack the API to become an Admin.
        


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
