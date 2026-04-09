from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Notice we import IsProvider here now
from accounts.permissions import IsSeeker, IsProvider
from .models import Booking
from .serializers import BookingSerializer, ProviderBookingSerializer

from .models import Booking, Transaction

from rest_framework.exceptions import ValidationError
from .serializers import ReviewSerializer


# --- SEEKER VIEWS ---

class CreateBookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsSeeker]

    def perform_create(self, serializer):
        seeker_profile = self.request.user.seeker_profile
        serializer.save(seeker=seeker_profile)

# --- PROVIDER VIEWS ---

class ProviderIncomingBookingsView(generics.ListAPIView):
    serializer_class = ProviderBookingSerializer
    permission_classes = [IsAuthenticated, IsProvider]

    def get_queryset(self):
        # Find the provider profile of the logged-in user
        provider_profile = self.request.user.provider_profile
        # Return only THEIR bookings, showing the newest first
        return Booking.objects.filter(service_provider__provider=provider_profile).order_by('-created_at')

class AcceptBookingView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):
        try:
            # Secure fetch: Make sure the booking exists AND belongs to this provider
            booking = Booking.objects.get(pk=pk, service_provider__provider=self.request.user.provider_profile)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or not assigned to you."}, status=status.HTTP_404_NOT_FOUND)

        # Business logic: You can only accept a PENDING booking
        if booking.status != Booking.StatusChoices.PENDING:
            return Response({"error": "Only pending bookings can be accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Update and save
        booking.status = Booking.StatusChoices.ACCEPTED
        booking.save()
        
        return Response({"message": f"Booking #{booking.id} has been ACCEPTED."}, status=status.HTTP_200_OK)
    

class CompleteBookingView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, service_provider__provider=self.request.user.provider_profile)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != Booking.StatusChoices.ACCEPTED:
            return Response({"error": "Only ACCEPTED bookings can be marked as COMPLETED."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Update Booking Status
        booking.status = Booking.StatusChoices.COMPLETED
        booking.save()

        # 2. Generate the Transaction Record (The Bill)
        # We pull the price directly from the Service model
        service_price = booking.service_provider.service.price
        
        transaction = Transaction.objects.create(
            booking=booking,
            transaction_type="CARD", # Defaulting to card for now
            amount=service_price,
            status=Transaction.StatusChoices.PENDING # Pending until the seeker pays
        )

        return Response({
            "message": f"Service completed. Transaction #{transaction.id} generated for ₹{transaction.amount}.",
            "booking_status": booking.status
        }, status=status.HTTP_200_OK)
    


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsSeeker]

    def perform_create(self, serializer):
        # Grab the booking ID from the URL (e.g., /api/bookings/1/review/)
        booking_id = self.kwargs.get('pk')
        
        try:
            # Rule 1: Ensure the booking belongs to this Seeker
            booking = Booking.objects.get(pk=booking_id, seeker__user=self.request.user)
        except Booking.DoesNotExist:
            raise ValidationError({"error": "Booking not found or you are not authorized to review it."})

        # Rule 2: Ensure the job is actually finished
        if booking.status != Booking.StatusChoices.COMPLETED:
            raise ValidationError({"error": "You can only review completed services."})

        # Rule 3: Prevent duplicate reviews (OneToOneField constraint check)
        if hasattr(booking, 'review'):
            raise ValidationError({"error": "You have already reviewed this booking."})

        # If all shields hold, save the review
        serializer.save(booking=booking, reviewer=self.request.user)