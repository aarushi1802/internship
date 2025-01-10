from django.contrib import admin
from .models import Order, Product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'product_name', 'quantity', 'calculated_order_value')
    search_fields = ('id', 'customer_name', 'customer_email')
    list_filter = ('product_name',)
    ordering = ('id',)

    def calculated_order_value(self, obj):
        return obj.order_value
    calculated_order_value.short_description = 'Order Value'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)
    ordering = ('id',)
