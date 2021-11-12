from django.db import models

from django.utils import timezone
from django.contrib.gis.db import models
from shortuuid.django_fields import ShortUUIDField

from apps.orders.models import Order
from apps.products.models import Product


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField()

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{order}, {product}, {quantity}, {total}".format(
            order=self.order.id,
            product=self.product.name,
            quantity=self.quantity,
            total=self.total
        )