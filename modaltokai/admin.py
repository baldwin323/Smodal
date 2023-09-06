from django.contrib import admin
from .models import SaleItem

#registering models to the admin interface
admin.site.register(SaleItem)