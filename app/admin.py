from django.contrib import admin
from .models import CustomerInfo, Category, Products, Kart


# Register your models here.


@admin.register(CustomerInfo)
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'user_image', 'locality', 'pincode', 'city', 'state', 'country',
                    'created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_id', 'name', 'description', 'price', 'slug', 'image', 'discount_price', 'label', 'created_at',
                    'updated_at']


@admin.register(Kart)
class KartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered', 'item', 'quantity']
