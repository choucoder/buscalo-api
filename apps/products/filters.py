from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price']