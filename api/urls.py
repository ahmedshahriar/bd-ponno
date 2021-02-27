from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('medicines/', views.ProductListView.as_view(), name='product_list'),
]
