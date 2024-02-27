from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street} {self.street_number}, {self.city}, {self.postal_code}, {self.country}'


class Order(models.Model):
    CART = 1
    PROCESSING = 2
    COMPLETED = 3
    CANCELLED = 4
    STATUS_CHOICES = [
        (CART, 'In Cart'),
        (PROCESSING, 'Being Processed'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('CC', 'Credit Card'),
        ('PP', 'PayPal'),
        ('COD', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_CHOICES, default='CC')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} - {self.name} {self.surname} - {self.get_status_display()}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
