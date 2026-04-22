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
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ServiceProvider
        fields = ['id', 'user_id', 'service', 'is_active']