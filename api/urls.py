from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
]
