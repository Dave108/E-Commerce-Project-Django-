from django.contrib import admin
from .models import CustomerInfo, Category, Products, Kart, OrderPlaced, CheckoutAddress, Payment, OrderedItems


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
    list_display = ['id', 'category_id', 'name', 'description', 'price', 'slug', 'image', 'discount_price', 'label',
                    'created_at',
                    'updated_at']


@admin.register(Kart)
class KartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered', 'item', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'start_date', 'ordered_date', 'ordered', 'original_price', 'final_price', 'payment_id']


@admin.register(CheckoutAddress)
class CheckoutAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'street_address', 'apartment_address', 'country', 'zip']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'timestamp', 'payment_choice']


@admin.register(OrderedItems)
class OrderedItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered', 'item', 'quantity']