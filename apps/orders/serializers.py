from rest_framework import serializers

from .models import Order, OrderProduct
from users.serializers import UserSerializer
from apps.shops.serializers import CreateShopSerializer
from apps.products.serializers import CreateProductSerializer


class ManyToManyOrderProductSerializer(serializers.ModelSerializer):
    product = CreateProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderProduct
        exclude = ['order']

# Order serializers
class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['user', 'shop']


class ListOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    shop = CreateShopSerializer(many=False, read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    shop = CreateShopSerializer(many=False, read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = (
            'id',
            'shop',
            'status',
            'total_order_price',
            'products'
        )

    def to_representation(self, instance):
        order_products = OrderProduct.objects.filter(order=instance)
        order_products_serialized = []
        for order_product in order_products:
            order_product_serializer = ManyToManyOrderProductSerializer(order_product)
            order_products_serialized.append(order_product_serializer.data)
        
        serialized_self = dict(super().to_representation(instance))
        serialized_self['products'] = order_products_serialized
        return serialized_self


# Order product serializers
class CreateOrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        exclude = ['order', 'product', 'total']


class ListOrderProductsSerializer(serializers.ModelSerializer):
    order = ListOrderSerializer(many=False, read_only=True)
    product = CreateProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderProduct
        fields = ('__all__')