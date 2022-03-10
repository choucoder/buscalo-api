from rest_framework_gis.serializers import GeoModelSerializer

from .models import Feedback


class FeedbackSerializer(GeoModelSerializer):
    class Meta:
        model = Feedback
        exclude = ['user']