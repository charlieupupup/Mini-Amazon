from django.contrib import admin

# Register your models here.
from .models import stock, warehouse, product

admin.site.register(stock)
admin.site.register(warehouse)
admin.site.register(product)