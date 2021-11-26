from datetime import datetime
from uuid import uuid4

import geopy
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from users.models import User
from core.utils import get_filename
from core.models import Address


class Shop(models.Model):
    id = ShortUUIDField(
        length=16,
        max_length=40,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, default="")

    address = models.OneToOneField(Address, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.PointField(geography=True, blank=True, null=True)
    logo = models.ImageField(upload_to=get_filename, blank=True, null=True)
    
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def update_address(self):
        if self.location and not self.address:
            try:
                locator = Nominatim(user_agent="google")
                coords = [str(coord) for coord in self.location.coords]
                str_coords = ", ".join(coords)

                location = locator.reverse(str_coords)
                data = location.raw
                if data:
                    address = Address(
                        country=data['address'].get('country', ""),
                        country_code=data['address'].get('country_code', ""),
                        state=data['address'].get('state', ""),
                        city=data['address'].get('county', ""),
                        address=data.get('display_name', "")
                    )
                    address.save()
                    self.address = address
                super().save()
            except:
                pass

    def __str__(self):
        return "{name}, {user}, {description}".format(
            name=self.name,
            user=self.user.first_name,
            description=self.description
        )