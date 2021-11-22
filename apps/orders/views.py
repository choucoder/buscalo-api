from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import Order, OrderProduct
from apps.products.models import Product

class OrderProductsAPIView(APIView):
    permission_classes = ()
    serializer_classes = {
        'list': ListOrderProductsSerializer,
        'create': CreateOrderProductsSerializer
    }
    default_serializer_class = CreateOrderProductsSerializer

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)

    def post(self, request, product_pk):
        user = request.user
        product = get_object_or_404(Product, pk=product_pk)
        
        if product.shop.user == user:
            return Response(
                {'data': {
                    "message": "You can not order a product of your own store"
                }},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer_class('create')(data=request.data)

        if serializer.is_valid():
            order = Order.objects.filter(user=user, status=Order.CREATED).first()
            if not order:
                order = Order(user=request.user, shop=product.shop)
                order.save()
            else:
                if order.shop != product.shop:
                    return Response(
                        {'data': {"message": "You only can to add products of the same store"}},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            o_products = OrderProduct.objects.filter(
                order=order, product=product
            )
            if o_products:
                o_product = o_products.first()
                o_product.quantity = request.data['quantity']
                o_product.total = o_product.product.price * request.data['quantity']
                o_product.save()
            else:
                total = request.data['quantity'] * product.price
                o_product = serializer.save(order=order, product=product, total=total)
            
            order.update_total_price()
            serializer = self.get_serializer_class('list')(o_product, many=False)
   
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MeOrdersAPIView(APIView):
    serializer_class = ListOrderSerializer

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
                           
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)