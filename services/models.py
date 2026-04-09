from django.db import models
from accounts.models import Provider

class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Adding a description is a standard practice, even if not in the initial DB schema
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    # This is the mapping table from your DB Schema
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='offered_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    # As discussed, we are using a string for now, but in production, 
    # this would ideally be a separate Availability table or a JSON/Array field.
    available_time = models.CharField(max_length=255, help_text="e.g., 10:00 AM - 05:00 PM")

    def __str__(self):
        return f"{self.provider.user.username} provides {self.service.name}"