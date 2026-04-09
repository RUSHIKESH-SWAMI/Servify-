from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    # AllowAny means you don't need to be logged in to access this page
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer