from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import GeometryDistance
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models import Currency
from core.views import PaginateAPIView

from .models import Shop
from .filters import ShopFilter
from .serializers import ListShopSerializer, CreateShopSerializer
from .permissions import IsShopOwner
from users.models import User, SearchSetting


class ShopsAPIView(PaginateAPIView):
    serializer_classes = {
        'list': ListShopSerializer,
        'create': CreateShopSerializer,
    }
    default_serializer_class = ListShopSerializer
    permission_classes = (IsShopOwner, )
    
    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)

    def get(self, request):
        user = request.user
        settings = SearchSetting.objects.filter(user=user).first()
        location = user.location if not settings.location else settings.location

        if location:
            shops = Shop.objects.filter(
                location__distance_lt=(
                    location,
                    Distance(m=settings.distance)
                )
            )
            shops = shops.filter().order_by(
                GeometryDistance("location", location)
            )
        else:
            shops = Shop.objects.all()

        f = ShopFilter(request.GET, queryset=shops)
        page = self.paginate_queryset(f.qs.order_by('created_at'))

        if page is not None:
            serializer = self.get_serializer_class('list')(page, many=True)
            return self.get_paginated_response(serializer.data)


    def post(self, request):
        user = request.user
        data = request.data
        currency = data.pop('currency', None)
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            currency = Currency.objects.filter(code=currency).first()
            
            if not "location" in data:
                shop = serializer.save(user=user, location=user.location, currency=currency)
            else:
                shop = serializer.save(user=user, currency=currency)
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
                    shop.save()
                    # shop.refresh_from_db()

            serializer.save()
            shop.update_address(is_location=is_location)
            
            serializer = self.get_serializer_class('list')(instance=shop)

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
