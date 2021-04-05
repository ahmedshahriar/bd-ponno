# from decimal import Decimal
# from products.fields import MongoDecimalField


# price = MongoDecimalField(max_length=10, decimal_places=2, blank=True, null=True, max_digits=10,
#                           default=Decimal(0.0))

# Create your models here.
# https://github.com/nesdis/djongo/pull/525/commits/86dbe3918ac4b2299d6aa3249a4509996f53920c

# add this code segment in  the djongo/operations.py file  and convert it to use DecimalField

# import bson
# def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
#     if value is None:
#         return None
#     return bson.Decimal128(super().adapt_decimalfield_value(value, max_digits, decimal_places))
# from django.template.defaultfilters import truncatechars
from django.core.validators import URLValidator
from djongo import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    product_url = models.URLField(blank=False, null=False, validators=[URLValidator])
    price = models.IntegerField(blank=True, null=True, default=0)
    image_url = models.URLField(blank=True, null=True, validators=[URLValidator])
    in_stock = models.BooleanField(blank=True, null=True)
    category = models.ArrayReferenceField(
        to=Category,
        on_delete=models.CASCADE,
    )
    tags = models.ArrayField(model_container=Tag,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "product"
        verbose_name_plural = 'products'
        indexes = [
            models.Index(fields=['name'], name='%(app_label)s_%(class)s_name_index'),
        ]

    # https://stackoverflow.com/questions/40275617/django-admin-truncate-text-in-list-display
    # @property
    # def short_name(self):
    #     # return self.name[:60]+'...'
    #     return truncatechars(self.name + '...', 35)

    def __str__(self):
        return self.name
