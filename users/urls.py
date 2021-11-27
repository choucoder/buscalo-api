from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', TestAPIView.as_view(), name='test'),
    path('users/', UsersApiView.as_view(), name='users'),
    path('me', MeUserAPIView.as_view(), name='user'),
    path('me/settings', MeUserSearchSettings.as_view(), name='me_search_settings_apiview'),
]