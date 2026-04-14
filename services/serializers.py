from rest_framework import serializers
from .models import Service, ServiceProvider
from .models import Category

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        
# (Keep your existing ServiceSerializer below this)

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ServiceProviderSerializer(serializers.ModelSerializer):
    # This will pull in the service details rather than just the ID number
    service = ServiceSerializer(read_only=True)
    provider_name = serializers.CharField(source='provider.user.username', read_only=True)

    class Meta:
        model = ServiceProvider
        fields = ['id', 'provider_name', 'service', 'available_time']