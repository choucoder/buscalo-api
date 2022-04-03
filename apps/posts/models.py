from uuid import uuid4

from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from users.models import User
from apps.products.models import Product
from apps.shops.models import Shop
from core.utils import get_filename


class Post(models.Model):
    # Notification type choices
    FEED = 0
    PUSH = 1
    # Post type choices
    HISTORY = 0
    PRODUCT = 1

    type_choices = [
        (HISTORY, 'HISTORY'),
        (PRODUCT, 'PRODUCT'),
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
    text = models.CharField(max_length=65565, null=True)
    photo = models.ImageField(upload_to=get_filename, blank=True, null=True)
    location = models.PointField(geography=True, blank=True, null=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    def set_view(self, request):
        self.views += 1
        super().save()

    def get_reactions_amount(self):
        return PostReaction.objects.filter(post=self).count()

    def __str__(self):
        if self.type_choices == self.PRODUCT:
            return "{shop}, {product}, {type}, {notify_type}".format(
                shop=self.shop.name,
                product=self.product.name,
                type=self.type,
                notify_type=self.get_notify_type_display()
            )
        else:
            return "{user}, {text}, {type}, {notify_type}".format(
                user=self.user.first_name,
                text=self.text,
                type=self.type,
                notify_type=self.get_notify_type_display()
            )


class PostReaction(models.Model):
    LOVE = 1

    reaction_choices = [
        (LOVE, 'LOVE'),
    ]

    id = ShortUUIDField(
        length=32,
        max_length=64,
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(
        choices=reaction_choices,
        default=reaction_choices[0][0]
    )

    def __str__(self):
        return "{user}, {product}, {rating}".format(
            user=self.user.first_name,
            product=self.product.name,
            rating=self.rating
        )