from django.urls import path
from .views import ServiceListView, ServiceProviderListView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('<int:service_id>/providers/', ServiceProviderListView.as_view(), name='service-providers'),
]