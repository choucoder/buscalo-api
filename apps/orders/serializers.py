from rest_framework import serializers

from .models import Order, OrderProduct
from users.serializers import UserSerializer
from apps.shops.serializers import CreateShopSerializer
from apps.products.serializers import CreateProductSerializer


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