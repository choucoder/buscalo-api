from django.urls import path
from .views import *


urlpatterns = [
    path('feedback', FeedbacksAPIView.as_view(), name='feedback_apiview'),
]