
from .models import Booking, Transaction
from .serializers import BookingSerializer, ProviderBookingSerializer, ReviewSerializer
import requests
from django.conf import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import ValidationError


# --- Inline Role Permissions (no accounts app needed) ---

class IsSeeker(BasePermission):
    message = "You must be a Seeker to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'SEEKER')


class IsProvider(BasePermission):
    message = "You must be a Provider to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'PROVIDER')


# --- SEEKER VIEWS ---

class CreateBookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsSeeker]

    def create(self, request, *args, **kwargs):
        # 1. Grab the ID the user is trying to book from the incoming JSON
        provider_id = request.data.get('service_provider_id')

        if not provider_id:
            return Response({"error": "service_provider_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. THE PHONE CALL: Ask Accounts on Port 8001 if this ID exists
        accounts_url = f"{settings.IDENTITY_SERVICE_URL}/api/accounts/profile/{provider_id}/"
        
        try:
            # We make a lightning-fast HTTP GET request to Microservice 1
            response = requests.get(accounts_url, timeout=5)
            
            if response.status_code != 200:
                # The Accounts server said this user doesn't exist (404)
                return Response(
                    {"error": f"Verification Failed: Provider ID {provider_id} does not exist in the Identity system."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except requests.exceptions.RequestException:
            # The Accounts server is completely offline/crashed
            return Response(
                {"error": "Identity service is currently unreachable. Cannot verify provider."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 3. IF WE REACH HERE, THE PROVIDER IS REAL. Save the booking!
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Pull seeker ID directly from the JWT token
        serializer.save(seeker_id=request.user.id) 
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MockPaymentVerificationView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def post(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(
                id=transaction_id,
                booking__seeker_id=request.user.id  # plain integer comparison
            )
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        if transaction.status == Transaction.StatusChoices.SUCCESS:
            return Response({"message": "This transaction is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        transaction.gateway_payment_id = f"pay_mock_{transaction.id}89X"
        transaction.gateway_signature = "mock_valid_signature_string"
        transaction.status = Transaction.StatusChoices.SUCCESS
        transaction.save()

        return Response({
            "message": "Payment verified successfully.",
            "transaction_id": transaction.id,
            "status": transaction.status,
            "gateway_payment_id": transaction.gateway_payment_id
        }, status=status.HTTP_200_OK)


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsSeeker]

    def perform_create(self, serializer):
        booking_id = self.kwargs.get('pk')

        try:
            booking = Booking.objects.get(pk=booking_id, seeker_id=self.request.user.id)
        except Booking.DoesNotExist:
            raise ValidationError({"error": "Booking not found or you are not authorized to review it."})

        if booking.status != Booking.StatusChoices.COMPLETED:
            raise ValidationError({"error": "You can only review completed services."})

        if hasattr(booking, 'review'):
            raise ValidationError({"error": "You have already reviewed this booking."})

        serializer.save(booking=booking, reviewer_id=self.request.user.id)


# --- PROVIDER VIEWS ---

class ProviderIncomingBookingsView(generics.ListAPIView):
    serializer_class = ProviderBookingSerializer
    permission_classes = [IsAuthenticated, IsProvider]

    def get_queryset(self):
        # Filter by provider's user ID directly from JWT
        return Booking.objects.filter(service_provider_id=self.request.user.id).order_by('-created_at')


class AcceptBookingView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, service_provider_id=request.user.id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or not assigned to you."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != Booking.StatusChoices.PENDING:
            return Response({"error": "Only pending bookings can be accepted."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.StatusChoices.ACCEPTED
        booking.save()

        return Response({"message": f"Booking #{booking.id} has been ACCEPTED."}, status=status.HTTP_200_OK)


class CompleteBookingView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, service_provider_id=request.user.id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != Booking.StatusChoices.ACCEPTED:
            return Response({"error": "Only ACCEPTED bookings can be marked as COMPLETED."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.StatusChoices.COMPLETED
        booking.save()

        # Amount will come from the request body since we can't query services DB
        amount = request.data.get('amount', 0)

        transaction = Transaction.objects.create(
            booking=booking,
            transaction_type="CARD",
            amount=amount,
            status=Transaction.StatusChoices.PENDING
        )

        return Response({
            "message": f"Service completed. Transaction #{transaction.id} generated for ₹{transaction.amount}.",
            "booking_status": booking.status
        }, status=status.HTTP_200_OK)