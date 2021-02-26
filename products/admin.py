from django.contrib import admin

# Register your models here.
from products.models import Product


@admin.register(Product)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'product_url', 'price', 'image_url', 'available')
    list_filter = ('vendor', 'available', 'type', 'created')
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('created',)