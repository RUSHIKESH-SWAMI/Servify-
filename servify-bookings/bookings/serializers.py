from rest_framework import serializers
from .models import Booking, Review, Transaction


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'seeker_id', 'service_provider_id', 'booking_date', 'booking_time', 'address', 'status']
        read_only_fields = ['seeker_id', 'status']


class ProviderBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'seeker_id', 'service_provider_id', 'booking_date', 'booking_time', 'address', 'status']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'reviewer_id', 'rating', 'review_text', 'created_at']
        read_only_fields = ['booking', 'reviewer_id']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'booking', 'transaction_type', 'amount', 'status', 'gateway_payment_id']
