from rest_framework import serializers

from .models import Shop
from users.serializers import UserSerializer


class ListShopSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Shop
        fields = ('__all__')


class CreateShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        exclude = ['user']