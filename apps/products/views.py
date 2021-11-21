from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ListProductSerializer, CreateProductSerializer
from .permissions import IsProductOwner
from apps.shops.models import Shop
from apps.shops.permissions import IsShopOwner


class ProductsAPIView(APIView):

    serializer = ListProductSerializer
    permission_classes = (IsProductOwner, )

    def get(self, request):
        data = request.data
        user = request.user

        if 'location' in data and user.location:
            if 'location' in data:
                point = Point(*data.pop('location'))
            else:
                point = user.location
            shops = Shop.objects.filter(
                location__distance_lt=(
                    point,
                    Distance(m=5000)
                )
            )
            products = Product.objects.filter(shop__in=shops, **data)
        else:
            products = Product.objects.filter(**data)
        serializer = self.serializer(products, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    

class ShopProductsAPIView(APIView):
    serializer_classes = {
        'list': ListProductSerializer,
        'create': CreateProductSerializer,
    }
    default_serializer_class = ListProductSerializer
    permission_classes = (IsShopOwner, )

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)
    
    def post(self, request, shop_pk):
        data = request.data
        shop = get_object_or_404(Shop, pk=shop_pk)
        self.check_object_permissions(request, shop)
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            product = serializer.save(shop=shop)
            serializer = self.get_serializer_class('list')(instance=product)
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def get(self, request, shop_pk):
        data = request.data
        shop = get_object_or_404(Shop, pk=shop_pk)
        products = Product.objects.filter(shop=shop, **data)
        serializer = self.get_serializer_class('list')(products, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class ProductAPIView(APIView):
    serializer_classes = {
        'list': ListProductSerializer,
        'create': CreateProductSerializer
    }
    default_serializer_class = ListProductSerializer
    permission_classes = (IsProductOwner, )

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer_class('list')(instance=product)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)
        serializer = self.get_serializer_class('create')(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class MeProductsAPIView(APIView):
    serializer_class = CreateProductSerializer
    permission_classes = (IsProductOwner, )

    def get(self, request):
        shops = Shop.objects.filter(user=request.user)
        products = Product.objects.filter(shop__in=shops)
        serializer = self.serializer_class(products, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
