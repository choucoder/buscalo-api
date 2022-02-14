from shortuuid.django_fields import ShortUUIDField
from django.db import models


class Address(models.Model):
    id = ShortUUIDField(
        length=16,
        max_length=32,
        primary_key=True,
        editable=False,
        alphabet='0123456789'
    )

    country = models.CharField(
        max_length=32
    )
    country_code = models.CharField(
        max_length=16, blank=True, null=True
    )
    state = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=1024, null=True, blank=True)


    def __str__(self):
        return "{country}, {state}, {city}, {address}".format(
            country=self.country,
            state=self.state,
            city=self.city,
            address=self.address
        )


class Currency(models.Model):
    id = ShortUUIDField(
        length=4,
        max_length=8,
        primary_key=True,
        editable=False,
        alphabet='123456789'
    )
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    country_code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return "{code}, {name}, {country}".format(
            code=self.code,
            name=self.name,
            country=self.country
        )