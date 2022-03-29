from django.urls import path
from .views import FeedAPIView, FeedsAPIView


urlpatterns = [
    path('feed/', FeedsAPIView.as_view(), name='feed'),
    path('feeds/<str:pk>', FeedAPIView.as_view(), name='feed_post_apiview'),
]