from django.urls import path
from .views import *


urlpatterns = [
    path('products', ProductsAPIView.as_view(), name='products_apiview'), # List all products
    path('products/<str:pk>', ProductAPIView.as_view(), name='product_apiview'), # Details
    path('me/products', MeProductsAPIView.as_view(), name='me_products_apiview'),
    path('shops/<str:shop_pk>/products', ShopProductsAPIView.as_view(), name='shop_products_apiview'), # List and Create new products
]