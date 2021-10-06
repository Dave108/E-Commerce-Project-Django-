from django.contrib import admin
from .models import CustomerInfo, Category, Products, ProductOrdered


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
    list_display = ['id', 'category_id', 'name', 'description', 'price', 'image', 'discount_price', 'label', 'created_at',
                    'updated_at']


@admin.register(ProductOrdered)
class ProductOrderedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered', 'item', 'quantity', 'total_price']
