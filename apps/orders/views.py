from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.orders.utils import abort_if_order_is_finished

from .serializers import *
from .models import Order, OrderProduct
from .permissions import IsOrderOwner
from apps.products.models import Product
from apps.shops.models import Shop


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

            abort_if_order_is_finished(order)
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


class OrderDetailsAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOrderOwner, )

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        serializer = self.serializer_class(order)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class CompleteOrderAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOrderOwner, )

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)

        if order.status != Order.CREATED:
            return Response(
                {"data": {"message": f"The order has already been marked as {order.get_status_display()}"}},
                status=status.HTTP_400_BAD_REQUEST 
            )
        
        order.status = Order.COMPLETED
        order.save()
        serializer = self.serializer_class(order)
        return Response(
            {"data": serializer.data}, status=status.HTTP_200_OK
        )


class CancelOrderAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOrderOwner, )

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)

        if order.status != Order.CREATED:
            return Response(
                {"data": {"message": f"The order has already been marked as {order.get_status_display()}"}},
                status=status.HTTP_400_BAD_REQUEST 
            )
        
        order.status = Order.CANCELLED
        order.save()
        serializer = self.serializer_class(order)
        return Response(
            {"data": serializer.data}, status=status.HTTP_200_OK
        )


class OrderProductAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOrderOwner, )

    def delete(self, request, order_pk, product_pk):
        order = get_object_or_404(Order, pk=order_pk)
        self.check_object_permissions(request, order)
        abort_if_order_is_finished(order)
        order_product = get_object_or_404(OrderProduct, order=order, pk=product_pk)
        order_product.delete()
        order.update_total_price()
        # Si la orden ya no tiene productos, esta se marca como cancelada
        order_products = OrderProduct.objects.filter(order=order)

        if not order_products:
            order.status = Order.CANCELLED
            order.save()

        serializer = self.serializer_class(order)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get(self, request, order_pk, product_pk):
        order = get_object_or_404(Order, pk=order_pk)
        self.check_object_permissions(request, order)
        order_product = get_object_or_404(OrderProduct, order=order, pk=product_pk)
        serializer = ManyToManyOrderProductSerializer(order_product)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class MeOrdersStoresAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOrderOwner, )

    def get(self, request, shop_pk):
        shop = get_object_or_404(Shop, pk=shop_pk, user=request.user)
        orders = Order.objects.filter(shop=shop)
        serializer = self.serializer_class(orders, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)