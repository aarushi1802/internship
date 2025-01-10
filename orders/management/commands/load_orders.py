import json
from django.core.management.base import BaseCommand
from orders.models import Order

class Command(BaseCommand):
    help = 'Load orders from a JSON file'

    def handle(self, *args, **kwargs):
        try:
            with open('orders.json', 'r') as file:
                orders = json.load(file)

            for order in orders:
                Order.objects.create(
                    order_id=order['order_id'],
                    customer_name=order['customer_name'],
                    customer_email=order['customer_email'],
                    product=order['product_name'],
                    quantity=order['quantity'],
                    order_value=order['order_value']
                )

            self.stdout.write(self.style.SUCCESS('Orders have been loaded successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The file orders.json was not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
