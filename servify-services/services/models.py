from django.db import models

# -- 1. The Parent Category --
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# -- 2. The Specific Service --
class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', null=True) 
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.base_price})"

# -- 3. The Provider Mapping (Microservice Version) --
class ServiceProvider(models.Model):
    # 1. We replace the ForeignKey with a simple IntegerField
    user_id = models.IntegerField() 
    
    # Notice we keep the ForeignKey for 'service' because the Service table 
    # lives right here in the exact same database!
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='providers')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # 2. We can no longer traverse to self.user.username, so we just print the ID
        return f"Provider ID {self.user_id} - {self.service.name}"