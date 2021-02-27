from django.shortcuts import render

# Create your views here.
# Create your views here.
from rest_framework import generics, permissions

from api.serializers import ProductSerializer
from products.models import Product


class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
