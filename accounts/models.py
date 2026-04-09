from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Defining the roles for Role-Based Access Control
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SEEKER = 'SEEKER', 'Seeker'
        PROVIDER = 'PROVIDER', 'Provider'

    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.SEEKER)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Seeker(models.Model):
    # OneToOne links this directly to the User table
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    def __str__(self):
        return f"Seeker: {self.user.username}"

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    def __str__(self):
        return f"Provider: {self.user.username}"