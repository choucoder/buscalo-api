from rest_framework_gis.serializers import GeoModelSerializer

from .models import Post
from users.serializers import UserSerializer
from apps.shops.serializers import CreateShopSerializer
from apps.products.serializers import CreateProductSerializer


class CreatePostSerializer(GeoModelSerializer):
    
    class Meta:
        model = Post
        exclude = ['user', 'shop', 'product', 'location']


class ListPostSerializer(GeoModelSerializer):

    user = UserSerializer(many=False, read_only=True)
    shop = CreateShopSerializer(many=False, read_only=True)
    product = CreateProductSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('__all__')