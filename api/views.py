from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination

from api.serializers import ProductSerializer
from products.models import Product


# Create your views here.
class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer

    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    pagination_class = PageNumberPagination


class ProductSearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    pagination_class = PageNumberPagination
