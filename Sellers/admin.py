from django.contrib import admin

from Sellers.models import Order, OrderItem,Log

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Log)


# Register your models here.
