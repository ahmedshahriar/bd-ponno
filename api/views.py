from django_filters import rest_framework as filters
from djongo.models import ArrayField
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from api.serializers import ProductSerializer, CategorySerializer
from products.models import Product, Category


# Create your views here.
# todo add dynamic search
# https://betterprogramming.pub/how-to-make-search-fields-dynamic-in-django-rest-framework-72922bfa1543

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    tags = filters.CharFilter(distinct=True, method='filter_tags')

    # https://django-filter.readthedocs.io/en/stable/ref/filters.html#method ***
    # Product.objects.filter(tags=[{'name': 'server'}, {'name': 'dell'}])
    def filter_tags(self, queryset, name, value):
        print(name, value, type(value))
        tag_list = [{'name': v.strip()} for v in value.split(',')]
        qs = queryset.filter(tags=tag_list)

        # todo : OR condition
        # mycode = 'print "hello world"'
        # exec(mycode)
        # print(tag_list)
        # code = None
        # for tag in tag_list:
        #     code += 'queryset.filter(' + Q(tags=[tag]) | + ')'

        # queryset.filter(Q(income__gte=5000) | Q(income__isnull=True))

        return qs

    # todo filter category
    # Product.objects.filter(category__id__in=['552','554'])
    # https://stackoverflow.com/questions/25943426/django-rest-framework-get-filter-on-manytomany-field
    # https://stackoverflow.com/questions/56097041/how-to-filter-data-in-drf-from-database-by-multiple-keywords
    # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview

    # category = filters.ModelMultipleChoiceFilter(
    #     field_name='category__id',
    #     to_field_name='id',
    #     queryset=Category.objects.all(),
    # )

    class Meta:
        model = Product
        fields = ['category', 'tags', 'in_stock', 'vendor', 'min_price', 'max_price']

        filter_overrides = {
            ArrayField: {
                'filter_class': filters.Filter,
                'extra': lambda f: {
                    'lookup_expr': 'in',
                },
            },
        }


class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer

    queryset = Product.objects.all()

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter

    search_fields = ['name']
    pagination_class = PageNumberPagination


class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CategorySerializer

    queryset = Category.objects.all()

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['name']
    pagination_class = PageNumberPagination
