from django.db import models
from accounts.models import Seeker
from services.models import ServiceProvider

class Booking(models.Model):
    # State management for the booking lifecycle
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE, related_name='bookings')
    # Notice we link to ServiceProvider (the mapping), not just the Service!
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings')
    
    booking_date = models.DateField()
    booking_time = models.TimeField()
    address = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} | {self.seeker.user.username} -> {self.service_provider.service.name}"

class Transaction(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='transaction')
    transaction_type = models.CharField(max_length=50, default="CARD") # e.g., UPI, CARD, CASH
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Txn #{self.id} for Booking #{self.booking.id}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    # The user writing the review (usually the Seeker)
    reviewer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # 1 to 5 stars
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Booking #{self.booking.id} - {self.rating} Stars"
    

