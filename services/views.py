from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Service, ServiceProvider, Category
from .serializers import ServiceSerializer, ServiceProviderSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ServiceFilter

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny] # Anyone can browse services

class ServiceProviderListView(generics.ListAPIView):
    serializer_class = ServiceProviderSerializer
    permission_classes = [AllowAny]

    # This filters providers based on the service ID passed in the URL
    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return ServiceProvider.objects.filter(service__id=service_id)
    

# Category List View
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] # Publicly accessible

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny] # Publicly accessible    


class ServiceSearchView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny] # Publicly accessible
    
    # Turn on Filtering, Text Searching, and Ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # A. Connect the complex filter we just built in filters.py
    filterset_class = ServiceFilter
    
    # B. Allow pure text search across these specific fields (?search=cleaning)
    search_fields = ['name', 'description']
    
    # C. Allow sorting by these fields (?ordering=base_price or ?ordering=-base_price)
    ordering_fields = ['base_price', 'name']