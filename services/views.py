from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Service, ServiceProvider
from .serializers import ServiceSerializer, ServiceProviderSerializer

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