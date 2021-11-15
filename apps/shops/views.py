from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Shop
from .serializers import ListShopSerializer, CreateShopSerializer
from .permissions import IsShopOwner
from users.models import User


class ShopsAPIView(APIView):
    serializer_classes = {
        'list': ListShopSerializer,
        'create': CreateShopSerializer,
    }
    default_serializer_class = ListShopSerializer
    permission_classes = (IsShopOwner, )
    
    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)

    def get(self, request):
        shops = Shop.objects.all()
        serializer = self.get_serializer_class('list')(shops, many=True)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            shop = serializer.save(user=request.user)
            serializer = self.get_serializer_class('list')(instance=shop)
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class ShopAPIView(APIView):
    serializer_classes = {
        'list': ListShopSerializer,
        'create': CreateShopSerializer,
    }
    default_serializer_class = ListShopSerializer

    permission_classes = (IsShopOwner, )

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)


    def patch(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, shop)
        serializer = self.get_serializer_class('create')(shop, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        serializer = self.get_serializer_class('list')(instance=shop)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    
    def delete(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, shop)
        shop.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
