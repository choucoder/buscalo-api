from django.urls import path
from .views import *


urlpatterns = [
    path('reports', ReportsAPIView.as_view(), name='reports_apiview'),
]