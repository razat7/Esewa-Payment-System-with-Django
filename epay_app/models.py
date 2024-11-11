from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    food_name = models.CharField(max_length=100)
    food_price = models.FloatField()
    images = models.ImageField(upload_to="food_images")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)  # Changed to auto_now for updated_at

    def __str__(self) -> str:
        return self.food_name


class Orders(models.Model):
    ordered_food = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customer_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)  # Changed to auto_now for updated_at

    def save(self, *args, **kwargs):
        # Calculate total_price based on product price and quantity
        if self.ordered_food and self.quantity:
            self.price = self.ordered_food.food_price * self.quantity
        super(Orders, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order of {self.quantity} {self.ordered_food.food_name}"
