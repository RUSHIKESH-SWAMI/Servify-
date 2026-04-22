from rest_framework import permissions

class IsSeeker(permissions.BasePermission):
    message = "You must be registered as a Seeker to book a service."

    def has_permission(self, request, view):
        # Check if they are logged in AND their role is SEEKER
        return bool(request.user and request.user.is_authenticated and request.user.role == 'SEEKER')

class IsProvider(permissions.BasePermission):
    message = "Only Providers can access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'PROVIDER')