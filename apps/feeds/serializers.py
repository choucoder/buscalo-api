from rest_framework_gis.serializers import GeoModelSerializer

from .models import Feed
from apps.posts.serializers import ListPostSerializer
from users.serializers import UserSerializer

class FeedSerializer(GeoModelSerializer):
    post = ListPostSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = Feed
        fields = ('__all__')