from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import PasswordResetOTP
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer


# -- 1. Registration View --
class RegisterView(generics.CreateAPIView):
    # AllowAny means you don't need to be logged in to access this page
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

# -- 2. NEW Logout View --
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # The frontend sends the refresh token when logging out
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            
            # This kills the token permanently in the database
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# -- 3. NEW Profile View --
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the profile of the person making the request
        return self.request.user
    

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny] # Anyone can request a reset

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Security: We still return 200 OK so hackers can't use this to guess registered emails
                return Response({"message": "If that email exists, an OTP has been sent."}, status=status.HTTP_200_OK)

            # Generate 6-digit OTP
            otp_code = get_random_string(length=6, allowed_chars='0123456789')

            # Update or create the OTP in the database
            PasswordResetOTP.objects.update_or_create(
                user=user,
                defaults={'otp': otp_code, 'created_at': timezone.now()}
            )

            # "Send" the email (will print to your terminal)
            send_mail(
                subject='Servify Password Reset',
                message=f'Your OTP for password reset is: {otp_code}. It expires in 10 minutes.',
                from_email='noreply@servify.com',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({"message": "If that email exists, an OTP has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                otp_record = PasswordResetOTP.objects.get(user=user)
            except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
                return Response({"error": "Invalid email or OTP."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if OTP matches and is not expired
            if otp_record.otp != otp:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not otp_record.is_valid():
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Reset the password securely
            user.set_password(new_password)
            user.save()

            # Destroy the OTP so it can't be used again
            otp_record.delete()

            return Response({"message": "Password has been successfully reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
