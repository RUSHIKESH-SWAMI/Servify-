import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    # Translates ?max_price=500 into base_price <= 500
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr='lte')
    
    # Translates ?category=1 into an exact match for the parent category ID
    category = django_filters.NumberFilter(field_name="category__id")
    
    # Translates ?name=cleaning into a case-insensitive partial text match
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['category', 'max_price', 'name']