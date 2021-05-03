from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from api.serializers import ProductSerializer
from products.models import Product


# Create your views here.
# todo add dynamic search
# https://betterprogramming.pub/how-to-make-search-fields-dynamic-in-django-rest-framework-72922bfa1543

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'in_stock', 'vendor', 'min_price', 'max_price']


class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer

    queryset = Product.objects.all()

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter

    search_fields = ['name']
    pagination_class = PageNumberPagination


