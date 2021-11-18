from rest_framework_gis.serializers import GeoModelSerializer

from .models import Shop
from users.serializers import UserSerializer


class ListShopSerializer(GeoModelSerializer):
    
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Shop
        fields = ('__all__')


class CreateShopSerializer(GeoModelSerializer):
    
    class Meta:
        model = Shop
        exclude = ['user']