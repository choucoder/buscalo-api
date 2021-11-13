from uuid import uuid4

from django.utils import timezone
from django.contrib.gis.db import models
from shortuuid.django_fields import ShortUUIDField

from users.models import User
from apps.products.models import Product
from apps.shops.models import Shop


def getFilename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "%s.%s" % (str(uuid4()).replace('-', ''), extension)

    return '/'.join(['images', new_filename])


class Post(models.Model):
    # Notification type choices
    FEED = 0
    PUSH = 1
    # Post type choices
    PRODUCT = 0
    HISTORY = 1

    type_choices = [
        (PRODUCT, 'PRODUCT'),
        (HISTORY, 'HISTORY'),
    ]
    notify_type_choices = [
        (FEED, 'FEED'),
        (PUSH, 'PUSH')
    ]

    id = ShortUUIDField(
        length=24,
        max_length=64,
        primary_key=True,
        editable=False,
        alphabet='0123456789'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    type = models.PositiveSmallIntegerField(
        choices=type_choices,
        default=type_choices[0][0]
    )
    notify_type = models.PositiveSmallIntegerField(
        choices=notify_type_choices,
        default=notify_type_choices[0][0]
    )
    text = models.CharField(max_length=255, null=True)
    photo = models.ImageField(upload_to=getFilename, blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.type_choices == self.PRODUCT:
            return "{shop}, {product}, {type}, {notify_type}".format(
                shop=self.shop.name,
                product=self.product.name,
                type=self.type,
                notify_type=self.notify_type
            )
        else:
            return "{user}, {text}, {type}, {notify_type}".format(
                user=self.user.first_name,
                text=self.text,
                type=self.type,
                notify_type=self.notify_type
            )