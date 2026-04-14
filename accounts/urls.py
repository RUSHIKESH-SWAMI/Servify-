from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, UserProfileView,PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    #Core Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'), # Gives you the JWT
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #Logout & Profile
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-profile/', UserProfileView.as_view(), name='profile_update'), # Same view, but we can use it for updates too

    #Password Reset
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


]