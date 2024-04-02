from django.contrib import admin

from store.models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image', 'membership']
    list_filter = ['first_name', 'last_name', 'email',]
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image', 'membership', 'birth_date', 'profile_image_url']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name', 'email']
