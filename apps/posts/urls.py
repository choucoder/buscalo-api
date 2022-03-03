from django.urls import path
from .views import *


urlpatterns = [
    path('me/posts', MePostsAPIView.as_view(), name='me_post_apiview'),
    path('posts', PostsAPIView.as_view(), name="posts_apiview"),
    path('posts/<str:pk>', PostAPIView.as_view(), name='post_apiview'),
    path('posts/<str:pk>/react', PostReactionAPIView.as_view(), name='post_reaction_apiview'),
    path('products/<str:pk>/posts', PostProductsAPIView.as_view(), name='post_products_apiview'),
]