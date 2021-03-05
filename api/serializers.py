from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'product_url', 'price', 'image_url', 'in_stock', 'created', 'updated']
