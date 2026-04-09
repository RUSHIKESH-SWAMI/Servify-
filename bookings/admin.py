from django.contrib import admin
from .models import Booking, Transaction, Review

admin.site.register(Booking)
admin.site.register(Transaction)
admin.site.register(Review)