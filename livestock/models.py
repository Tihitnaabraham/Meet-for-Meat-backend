from django.db import models
from users.models import User

class Livestock(models.Model):
    breed = models.CharField(max_length=50)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    health_status = models.CharField(max_length=50)
    price_total = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=50)
    image = models.ImageField(upload_to='livestock_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.breed} ({self.weight_kg} kg)"
