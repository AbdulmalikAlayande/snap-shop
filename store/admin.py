from django.contrib import admin

from store.models import *


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'password', 'phone_number']
    list_filter = ['first_name', 'last_name', 'email',]
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'birth_date']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
