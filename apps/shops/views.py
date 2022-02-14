from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models import Currency

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
        user = request.user
        data = request.data
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            if not "location" in data:
                shop = serializer.save(user=user, location=user.location)
            else:
                shop = serializer.save(user=user)
            shop.update_address(is_location=True)

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
        data = request.data
        currency = data.pop('currency', None)
        is_location = bool(data.get('location', ""))

        self.check_object_permissions(request, shop)
        serializer = self.get_serializer_class('create')(shop, data=data, partial=True)

        if serializer.is_valid():
            if currency:
                currency = Currency.objects.filter(code=currency).first()
                if currency:
                    shop.currency = currency
                    shop.update()

            serializer.save()
            shop.update_address(is_location=is_location)
            
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


class MeShopsAPIView(APIView):

    serializer_class = ListShopSerializer
    permission_classes = (IsShopOwner, )

    def get(self, request):
        shops = Shop.objects.filter(user=request.user)
        serializer = self.serializer_class(shops, many=True)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )


class MeShopAPIView(APIView):

    serializer_class = ListShopSerializer
    permission_classes = (IsShopOwner, )

    def get(self, request):
        shop = get_object_or_404(Shop, user=request.user)
        serializer = self.serializer_class(instance=shop)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
