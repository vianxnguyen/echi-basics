from django.contrib import admin
from .models import Item, OrderItem, Order, ShippingInfo, Customer

# Register your models here.
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(ShippingInfo)