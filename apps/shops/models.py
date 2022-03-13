from datetime import datetime
from uuid import uuid4

import geopy
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User
from core.utils import get_filename, clean_str
from core.models import Address, Currency


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
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True)
    logo = models.ImageField(upload_to=get_filename, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def update_address(self, is_location=False):
        if self.location and is_location:
            try:
                locator = Nominatim(user_agent="google")
                coords = [str(coord) for coord in self.location.coords]
                str_coords = ", ".join(coords)

                location = locator.reverse(str_coords)
                data = location.raw
                if data:
                    if not self.address:
                        address = Address(
                            country=clean_str(data['address'].get('country', "")),
                            country_code=clean_str(data['address'].get('country_code', "")),
                            state=clean_str(data['address'].get('state', "")),
                            city=clean_str(data['address'].get('county', "")),
                            address=data.get('display_name', "")
                        )
                        address.save()
                        self.address = address
                        super().save()
                    else:
                        country = clean_str(data['address'].get('country', ""))
                        country_code = clean_str(data['address'].get('country_code', ""))
                        state = clean_str(data['address'].get('state', ""))
                        city = clean_str(data['address'].get('county', ""))
                        addr = clean_str(data.get('display_name', ""))

                        Address.objects.filter(id=self.address.id).delete()
                        address = Address(
                            country=country,
                            country_code=country_code,
                            state=state,
                            city=city,
                            address=addr
                        )
                        address.save()
                        self.address = address
                        super().save()
            except Exception as e:
                pass

    def __str__(self):
        return "{name}, {user}, {description}".format(
            name=self.name,
            user=self.user.first_name,
            description=self.description
        )