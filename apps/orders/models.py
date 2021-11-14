from uuid import uuid4

from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from apps.shops.models import Shop
from users.models import User


class Order(models.Model):
    CREATED = 1
    COMPLETED = 2
    EXPIRED = 3
    CANCELLED = 4

    id = ShortUUIDField(
        length=18,
        max_length=24,
        alphabet='1234567890',
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    details = models.CharField(max_length=255, null=True)
    total_order_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    status_choices = [
        (CREATED, 'CREATED'),
        (COMPLETED, 'COMPLETED'),
        (EXPIRED, 'EXPIRED'),
        (CANCELLED, 'CANCELED'),
    ]
    status = models.PositiveSmallIntegerField(
        default=status_choices[0][0],
        choices=status_choices
    )

    def __str__(self):
        return "{id}, {user}, {shop}, {status}".format(
            id=self.id,
            user=self.user.first_name,
            shop=self.shop.name,
            status=self.get_status_display()
        )
