from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from products.models import Product


@admin.register(Product)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'show_product_url', 'price', 'image_url', 'available')
    list_filter = ('vendor', 'available', 'type', 'created')
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('created',)

    # https://stackoverflow.com/a/31745953/11105356
    def show_product_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.product_url)

    show_product_url.short_description = "Product URL"
