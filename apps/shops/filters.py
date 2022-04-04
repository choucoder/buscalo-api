from django_filters import rest_framework as filters
from .models import Shop


class ShopFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Shop
        fields = ['name', 'description']