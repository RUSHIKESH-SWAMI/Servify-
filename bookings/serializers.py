from rest_framework import serializers
from .models import Booking
from .models import Review

class BookingSerializer(serializers.ModelSerializer):
    # Make the Seeker read-only. We will pull this securely from the JWT token, 
    # so users cannot forge bookings for other people.
    seeker = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'seeker', 'service_provider', 'booking_date', 'booking_time', 'address', 'status']
        read_only_fields = ['status'] # Seekers shouldn't be able to force a 'COMPLETED' status upon creation


class ProviderBookingSerializer(serializers.ModelSerializer):
    # These read-only fields "flatten" the related data so it's easy to read
    seeker_name = serializers.CharField(source='seeker.user.username', read_only=True)
    seeker_phone = serializers.CharField(source='seeker.user.phone_number', read_only=True)
    service_name = serializers.CharField(source='service_provider.service.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'seeker_name', 'seeker_phone', 'service_name', 
            'booking_date', 'booking_time', 'address', 'status'
        ]



class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'booking', 'reviewer_name', 'rating', 'review_text', 'created_at']
        read_only_fields = ['booking'] # We inject this securely in the view