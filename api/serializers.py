from rest_framework import serializers

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.DictField())
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'product_url', 'price', 'image_url', 'in_stock', 'category', 'tags',
                  'created', 'updated']
