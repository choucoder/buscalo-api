from django.urls import path

from .views import *


urlpatterns = [
    path('products/<str:product_pk>/add-to-order', OrderProductsAPIView.as_view(), name='order_products_apiview'),
    path('me/orders', MeOrdersAPIView.as_view(), name='me_orders_apiview'), # User
    # path('me/stores/<str:pk>/orders'),
    # path('orders/<str:pk>/complete'),
    # path('orders/<str:pk>/cancell'),
    # path('orders/<str:pk>/') # Order details 
]