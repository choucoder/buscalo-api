from rest_framework import serializers

from .models import Post
from users.serializers import UserSerializer
from apps.shops.serializers import CreateShopSerializer
from apps.products.serializers import CreateProductSerializer


class CreatePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        exclude = ['user', 'shop', 'product']


class ListPostSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False, read_only=True)
    shop = CreateShopSerializer(many=False, read_only=True)
    product = CreateProductSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('__all__')