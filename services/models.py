from django.db import models

# -- 1. The Parent Category --
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories" # Fixes the spelling in the Django Admin panel

# -- 2. The Specific Service --
class Service(models.Model):
    # The ForeignKey links this service to a parent category. 
    # null=True ensures your database doesn't crash if you already have services saved.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', null=True) 
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.base_price})"

# -- 3. The Provider Mapping (From Phase 2) --
class ServiceProvider(models.Model):
    # This assumes you have the User model imported or referenced. 
    # If your User model is in the 'accounts' app, we reference it as 'accounts.User'
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='offered_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='providers')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"