from django.urls import path
from .views import FeedsAPIView


urlpatterns = [
    path('feed/', FeedsAPIView.as_view(), name='feed')
]