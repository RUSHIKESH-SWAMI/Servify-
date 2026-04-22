from django.contrib import admin
from .models import Service, ServiceProvider ,Category

admin.site.register(Service)
admin.site.register(ServiceProvider)
admin.site.register(Category)