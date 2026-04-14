from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_id = models.IntegerField()

    quantity = models.IntegerField()

    phone = models.CharField(max_length=20)

    email = models.EmailField()

    address = models.TextField()

    payment_type = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)