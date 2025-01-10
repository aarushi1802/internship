from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField()
    order_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        # Calculate order_value using the linked Product's price
        if self.product_name and self.quantity:
            self.order_value = self.quantity * self.product_name.price
        super().save(*args, **kwargs)

    @property
    def order_id(self):
        return f"ORD-{self.id}"

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"
