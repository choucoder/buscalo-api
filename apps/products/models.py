from uuid import uuid4

from django.db.models import Sum
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from core.utils import get_filename
from apps.shops.models import Shop
from users.models import User


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

    def compute_rating(self):
        votes = Rating.objects.filter(product=self)
        votes_sum = votes.aggregate(Sum('rating'))['rating__sum']

        if votes_sum == None:
            rating = 0
        else:
            rating = votes_sum / votes.count()
        return rating

    def get_votes_amount(self):
        return Rating.objects.filter(product=self).count()

    def __str__(self):
        return "{id}, {shop}, {name}, {price}, {details}".format(
            id=self.id,
            name=self.name,
            shop=self.shop.name,
            price=self.price,
            details=self.details
        )


class Rating(models.Model):
    id = ShortUUIDField(
        length=24,
        max_length=64,
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{user}, {product}, {rating}".format(
            user=self.user.first_name,
            product=self.product.name,
            rating=self.rating
        )