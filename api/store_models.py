from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.name} on {self.date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order}"
