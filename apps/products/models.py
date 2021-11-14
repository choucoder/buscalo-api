from uuid import uuid4

from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from core.utils import get_filename
from apps.shops.models import Shop


class Product(models.Model):
    id = ShortUUIDField(
        length=16,
        max_length=40,
        primary_key=True,
        editable=False,
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    details = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    photo = models.ImageField(upload_to=get_filename, blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    status_choices = [
        (1, 'ACTIVE'),
    ]
    status = models.PositiveSmallIntegerField(
        default=status_choices[0][0],
        choices=status_choices
    )

    def __str__(self):
        return "{id}, {shop}, {name}, {price}, {details}".format(
            id=self.id,
            name=self.name,
            shop=self.shop.name,
            price=self.price,
            details=self.details
        )