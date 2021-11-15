from django.urls import path


urlpatterns = [
    path('/products'), # List all products
    path('/products/<str:pk>'), # Details
    path('/shops/<str:shop_pk>/products'), # List and Create new products
    path('/shops/<str:shop_pk>/products/<str:pk>'), # Update and delete products 
]