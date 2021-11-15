from rest_framework import serializers

from .models import Product
from apps.shops.serializers import ListShopSerializer, CreateShopSerializer


class ListProductSerializer(serializers.ModelSerializer):
    
    shop = ListShopSerializer(many=False, read_only=True)
    
    class Meta:
        model = Product
        fields = ('__all__')


class CreateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('__all__')
        exclude = ['shop']