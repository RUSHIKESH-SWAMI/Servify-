from django.urls import path
from .views import CreateBookingView, ProviderIncomingBookingsView, AcceptBookingView, CompleteBookingView, MockPaymentVerificationView, CreateReviewView

urlpatterns = [
    # Seeker Routes
    path('request/', CreateBookingView.as_view(), name='create-booking'),
    path('pay/<int:transaction_id>/', MockPaymentVerificationView.as_view(), name='verify-payment'),
    path('<int:pk>/review/', CreateReviewView.as_view(), name='create-review'), # <-- New Route
    
    # Provider Routes
    path('incoming/', ProviderIncomingBookingsView.as_view(), name='incoming-bookings'),
    path('<int:pk>/accept/', AcceptBookingView.as_view(), name='accept-booking'),
    path('<int:pk>/complete/', CompleteBookingView.as_view(), name='complete-booking'),
]