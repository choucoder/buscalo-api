from django.db import models


class Address(models.Model):
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