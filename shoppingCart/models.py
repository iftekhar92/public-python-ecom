from django.db import models
from django.contrib.auth.models import User
from productCatalogue.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

class Order(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=150)
    pin_code = models.CharField(max_length=10)
    full_address = models.CharField(max_length=200)
    payment_mode = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    total_amount = models.FloatField(default=0)
    status = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)
    order_items = models.ManyToManyField(OrderItems)
