from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from api.serializers import ProductSerializer
from products.models import Product


# Create your views here.
class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
