from rest_framework_gis.serializers import GeoModelSerializer

from .models import Feed
from apps.posts.serializers import ListPostSerializer


class FeedSerializer(GeoModelSerializer):
    post = ListPostSerializer(many=False, read_only=True)

    class Meta:
        model = Feed
        exclude = ['user']