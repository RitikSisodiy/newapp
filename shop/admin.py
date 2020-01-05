from django.contrib import admin

# Register your models here.
from .models import Product,order,OrderUpdate
admin.site.register(Product)
admin.site.register(order)
admin.site.register(OrderUpdate)