import csv
import datetime

from django.contrib import admin
# Register your models here.
from django.http import HttpResponse
from django.utils.html import format_html

from products.models import Product


def export_to_csv(model_admin, request, queryset):
    opts = model_admin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many \
              and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_display = ('name', 'vendor', 'show_product_url', 'show_image_url', 'price', 'in_stock')
    list_filter = ('vendor', 'in_stock', 'created')
    search_fields = ('name',)
    # date_hierarchy = 'created'  # todo needs to workaround with djongo
    ordering = ('created',)
    actions = [export_to_csv]

    # https://stackoverflow.com/a/31745953/11105356
    def show_product_url(self, obj):
        return format_html("<a target=”_blank” href='{url}'>{url}</a>", url=obj.product_url)

    def show_image_url(self, obj):
        return format_html("<a target=”_blank” href='{url}'>{url}</a>", url=obj.image_url)

    show_product_url.short_description = "Product URL"
    show_image_url.short_description = "Image URL"
