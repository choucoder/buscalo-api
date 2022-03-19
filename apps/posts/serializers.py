import datetime

from rest_framework_gis.serializers import GeoModelSerializer

from .models import Post, PostReaction
from users.serializers import UserSerializer
from apps.shops.serializers import CreateShopSerializer
from apps.products.serializers import CreateProductSerializer
from core.utils import get_time_ago


class CreatePostSerializer(GeoModelSerializer):
    class Meta:
        model = Post
        exclude = ['user', 'shop', 'product', 'location']

    def to_representation(self, instance):
        serialized_self = dict(super().to_representation(instance))
        serialized_self['reactions'] = instance.get_reactions_amount()
        return serialized_self


class ListPostSerializer(GeoModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    shop = CreateShopSerializer(many=False, read_only=True)
    product = CreateProductSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('__all__')

    def to_representation(self, instance):
        serialized_self = dict(super().to_representation(instance))
        serialized_self['reactions'] = instance.get_reactions_amount()
        current_date = datetime.datetime.today()
        created_date = instance.created_at
        created_date = created_date.replace(tzinfo=None)
        serialized_self['ago'] = get_time_ago(created_date, current_date)
        return serialized_self


class PostReactionSerializer(GeoModelSerializer):
    class Meta:
        model = PostReaction
        exclude = ['user', 'post']