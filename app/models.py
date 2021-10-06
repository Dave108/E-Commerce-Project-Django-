from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.

class CustomerInfo(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    # user_image = models.TextField()
    # cloudinary
    user_image = CloudinaryField('image')
    # ------
    locality = models.CharField(max_length=50)
    pincode = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_all_details(self):
        if len(self.gender) >= 0 and len(self.locality) >= 0 and len(self.city) >= 0 and len(self.state) >= 0 and len(self.country) >= 0:
            return True
        else:
            return False


class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


LABEL = (
    ('New', 'New'),
    ('Best Seller', 'Best Seller'),
    ('Clearance', 'Clearance'),
    ('Ever Green', 'Ever Green'),
)


class Products(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0)
    # cloudinary
    image = CloudinaryField('image')
    # ----------
    discount_price = models.FloatField(blank=True, null=True)
    label = models.CharField(choices=LABEL, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductOrdered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()
