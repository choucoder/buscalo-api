from django.urls import path
from .views import *


urlpatterns = [
    path('shops/', ShopsAPIView.as_view(), name='shops_apiview'),
    path('shops/<str:pk>', ShopAPIView.as_view(), name='shop_apiview'),
    path('me/shops', MeShopsAPIView.as_view(), name='me_shops_apiview'),
    path('me/shop', MeShopAPIView.as_view(), name='me_shop_apiview'),
]