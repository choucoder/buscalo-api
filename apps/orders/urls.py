from django.urls import path

from .views import *


urlpatterns = [
    path('products/<str:product_pk>/add-to-order', OrderProductsAPIView.as_view(), name='order_products_apiview'),
    path('me/orders', MeOrdersAPIView.as_view(), name='me_orders_apiview'), # User
    path('me/shops/<str:shop_pk>/orders', MeOrdersStoresAPIView.as_view(), name='me_orders_stores_apiview'),
    path('orders/<str:order_pk>/products/<str:product_pk>', OrderProductAPIView.as_view(), name='order_product_apiview'),
    path('orders/<str:pk>/complete', CompleteOrderAPIView.as_view(), name='complete_order_apiview'),
    path('orders/<str:pk>/cancell', CancelOrderAPIView.as_view(), name='cancel_order_apiview'),
    path('orders/<str:pk>', OrderDetailsAPIView.as_view(), name='order_details_apiview') # Order details 
]