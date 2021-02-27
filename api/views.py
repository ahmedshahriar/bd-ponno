from rest_framework import generics, permissions

from api.serializers import ProductSerializer
from products.models import Product


# Create your views here.
class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
