from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import UserSerializer
from .permissions import IsAllowedUser


class TestAPIView(APIView):

    def get(self, request):
        reply = {'data': {'message': 'Hello, world'}}
        print(request.user)
        return Response(reply, status=200, content_type='application/json')


class UsersApiView(APIView):

    serializer_class = UserSerializer
    permission_classes = ()

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        reply = {}
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            reply['data'] = serializer.data
            return Response(reply, status=status.HTTP_201_CREATED)
        else:
            reply['errors'] = serializer.errors
            return Response(reply, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):

    serializers_class = UserSerializer
    permission_classes = (IsAllowedUser, )

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
