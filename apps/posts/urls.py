from django.urls import path
from .views import *


urlpatterns = [
    path('posts', PostsAPIView.as_view(), name="posts_apiview"),
    path('posts/<str:pk>', PostAPIView.as_view(), name='post_apiview'),
    path('me/posts', MePostAPIView.as_view(), name='me_post_apiview'),
    path('products/<str:pk>/posts', PostProductsAPIView.as_view(), name='post_products_apiview'),
]