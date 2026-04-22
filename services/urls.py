from django.urls import path
from .views import (
    ServiceListView, 
    ServiceProviderListView, 
    CategoryListView, 
    ServiceDetailView,
    ServiceSearchView 
)

urlpatterns = [
    # Master list
    path('', ServiceListView.as_view(), name='service-list'),
    
    # Categories 
    path('categories/', CategoryListView.as_view(), name='category_list'),
    
    # 2. NEW: The Search API (Crucially placed ABOVE the <int:pk> route)
    path('search/', ServiceSearchView.as_view(), name='service-search'),
    
    # Detail view
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    # Providers for a service
    path('<int:service_id>/providers/', ServiceProviderListView.as_view(), name='service-providers'),
]