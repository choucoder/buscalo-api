from uuid import uuid4

from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from apps.shops.models import Shop


def getFilename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "%s.%s" % (str(uuid4()).replace('-', ''), extension)

    return '/'.join(['images', new_filename])


class Product(models.Model):
    id = ShortUUIDField(
        length=16,
        max_length=40,
        primary_key=True,
        editable=False,
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, required=True)
    details = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    photo = models.ImageField(upload_to=getFilename, blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    status_choices = [
        (1, 'ACTIVE'),
    ]
    status = models.PositiveSmallIntegerField(
        default=status_choices[0][0],
        choices=status_choices
    )