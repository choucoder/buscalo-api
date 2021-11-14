from datetime import datetime
from uuid import uuid4

from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from users.models import User
from core.utils import get_filename


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
    
    location = models.PointField(geography=True, blank=True, null=True)
    logo = models.ImageField(upload_to=get_filename, blank=True, null=True)
    
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{name}, {user}, {description}".format(
            name=self.name,
            user=self.user.first_name,
            description=self.description
        )