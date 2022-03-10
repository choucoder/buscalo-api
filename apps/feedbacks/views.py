from django.contrib.gis.measure import Distance
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Feedback
from .serializers import FeedbackSerializer
from core.views import PaginateAPIView
from users.models import User


class FeedbacksAPIView(PaginateAPIView):

    serializer_classes = {
        'create': FeedbackSerializer,
    }
    default_serializer_class = FeedbackSerializer

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)
    
    def post(self, request):
        data = request.data
        user = request.user

        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            feedback = serializer.save(user=user)

            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )