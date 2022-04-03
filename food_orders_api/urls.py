"""food_orders_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

prefix = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(prefix, include('users.urls')),
    path(prefix, include('apps.shops.urls')),
    path(prefix, include('apps.products.urls')),
    path(prefix, include('apps.posts.urls')),
    path(prefix, include('apps.orders.urls')),
    path(prefix, include('apps.feeds.urls')),
    path(prefix, include('apps.feedbacks.urls')),
    path(prefix, include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
