from djongo import models


# Create your models here.
class Product(models.Model):
    vendor = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    product_url = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_length=10, decimal_places=2, blank=True, null=True, max_digits=10)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    available = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "product"
        verbose_name_plural = 'products'
        indexes = [
            models.Index(fields=['name'], name='%(app_label)s_%(class)s_name_index'),
        ]

    def __str__(self):
        return self.name
