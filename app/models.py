from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.shortcuts import reverse, HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        if len(self.gender) >= 0 and len(self.locality) >= 0 and len(self.city) >= 0 and len(self.state) >= 0 and len(
                self.country) >= 0:
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
    slug = models.SlugField(max_length=250, null=True, blank=True)
    # cloudinary
    image = CloudinaryField('image')
    # ----------
    discount_price = models.FloatField(blank=True, null=True)
    label = models.CharField(choices=LABEL, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_product_url(self):
        return reverse("product", kwargs={
            "slug": self.slug
        })

    def get_add_checkout_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_checkout_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })

    def get_increase_cart_url(self):
        return reverse("increase-cart", kwargs={
            "pk": self.pk
        })

    def get_decrease_cart_url(self):
        return reverse("decrease-cart", kwargs={
            "pk": self.pk
        })


class Kart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"


@receiver(post_save, sender=Products)
# Now Creating a Function which will automatically insert slug when product is created
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        if not instance.slug:
            data = instance.name.lower()
            slug_data = str(data.replace(" ", "-"))
            exist_slug = Products.objects.filter(slug=slug_data).exists()
            print(exist_slug)
            if exist_slug:
                instance.slug = str(slug_data) + str(instance.pk)
                instance.save()
            else:
                instance.slug = slug_data
                instance.save()
    else:
        if not instance.slug:
            data = instance.name.lower()
            slug_data = str(data.replace(" ", "-"))
            exist_slug = Products.objects.filter(slug=slug_data).exists()
            print(exist_slug)
            if exist_slug:
                instance.slug = str(slug_data) + str(instance.pk)
                instance.save()
            else:
                instance.slug = slug_data
                instance.save()
