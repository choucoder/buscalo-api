from rest_framework import serializers

from .models import Product, Rating
from apps.shops.serializers import ListShopSerializer, CreateShopSerializer


class ListProductSerializer(serializers.ModelSerializer):
    
    shop = ListShopSerializer(many=False, read_only=True)
    
    class Meta:
        model = Product
        fields = ('__all__')

    def to_representation(self, instance):
        serialized_self = dict(super().to_representation(instance))
        serialized_self['rating'] = instance.compute_rating()
        serialized_self['votes_amount'] = instance.get_votes_amount()
        return serialized_self


class CreateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = ['shop']
    
    def to_representation(self, instance):
        serialized_self = dict(super().to_representation(instance))
        serialized_self['rating'] = instance.compute_rating()
        serialized_self['votes_amount'] = instance.get_votes_amount()
        return serialized_self


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['user', 'product']