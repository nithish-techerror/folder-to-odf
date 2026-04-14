from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):

    STATUS = [
        ("orderplaced", "Order Placed"),
        ("shipped", "Shipped"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    payment_type = models.CharField(max_length=50)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=50, choices=STATUS, default="orderplaced")

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.product.title