from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from users.models import User


class Feedback(models.Model):
    id = ShortUUIDField(
        length=24,
        max_length=32,
        primary_key=True,
        editable=False,
        alphabet='0123456789abcdefghijklmnopqrstuvwxyz'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=4096)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{user}, {text}".format(
            user=self.user.first_name,
            text=self.text
        )
