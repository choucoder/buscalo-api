from rest_framework_gis.serializers import GeoModelSerializer

from .models import Report
from apps.posts.serializers import ListPostSerializer
from apps.products.serializers import ListProductSerializer
from users.serializers import UserSerializer


class ReportSerializer(GeoModelSerializer):
    post = ListPostSerializer(many=False, read_only=True)
    product = ListProductSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)
    reported_by = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = Report
        fields = ('__all__')


class CreateReportSerializer(GeoModelSerializer):
    class Meta:
        model = Report
        exclude = ['post', 'product', 'created_by', 'reported_by']