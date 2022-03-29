import time
from functools import partial
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import SearchSetting, User
from .serializers import SearchSettingSerializer, UserSerializer
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
            if user.location:
                user.update_address()
            SearchSetting(user=user, location=user.location).save()
            
            reply['data'] = serializer.data
            return Response(reply, status=status.HTTP_201_CREATED)
        else:
            reply['errors'] = serializer.errors
            return Response(reply, status=status.HTTP_400_BAD_REQUEST)


class MeUserAPIView(APIView):

    serializers_class = UserSerializer
    permission_classes = (IsAllowedUser, )

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            user.update_address()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        user = request.user
        self.check_object_permissions(request, user)
        user.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class MeUserSearchSettings(APIView):
    serializer_class = SearchSettingSerializer

    def patch(self, request):
        user = request.user
        settings = SearchSetting.objects.filter(user=user).first()
        serializer = self.serializer_class(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            user.update_address()

            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 
    def get(self, request):
        settings = get_object_or_404(SearchSetting, user=request.user)
        serializer = self.serializer_class(settings)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class BotUsers(APIView):
    serializer_class = UserSerializer
    permission_classes = ()

    def post(self, request):
        data = request.data
        if "bot_username" in data and "bot_password" in data:
            username = data.get('bot_username')
            password = data.get('bot_password')

            if username == "buscalo" and password == "buscalopassword":
                user_id = data.get('telegram_user_id')
                user = get_object_or_404(User, telegram_user_id=user_id)
                serializer = self.serializer_class(instance=user)
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)     
            else:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({}, status=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)