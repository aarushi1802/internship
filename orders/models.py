from django.db import models

# Create your models here.
from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)  # Unique order ID
    customer_name = models.CharField(max_length=255)  # At least 3 characters
    customer_email = models.EmailField()  # Valid email format
    product = models.CharField(max_length=50, choices=[('Product 1', 'Product 1'), ('Product 2', 'Product 2'), ('Product 3', 'Product 3')])
    quantity = models.PositiveIntegerField()  # Greater than 0
    order_value = models.DecimalField(max_digits=10, decimal_places=2)  # Calculated value

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"
