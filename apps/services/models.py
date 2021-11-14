from django.contrib.gis.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

from users.models import User


class Service(models.Model):
    id = ShortUUIDField(
        length=16,
        primary_key=True,
        editable=False
    )
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0)
    amout = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{id}, {name}, {price}, {amount}".format(
            id=self.id,
            name=self.name,
            price=self.price,
            amount=self.amout
        )


class ServiceBuy(models.Model):
    NON_VERIFIED = 1
    DENIED = 2
    ACEPTED = 3

    id = ShortUUIDField(
        length=24,
        primary_key=True,
        editable=False,
        alphabet='0123456789'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    total = models.FloatField()
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    status_choices = [
        (NON_VERIFIED, 'NON_VERIFIED'),
        (DENIED, 'DENIED'),
        (ACEPTED, 'ACEPTED')
    ]
    status = models.PositiveSmallIntegerField(
        choices=status_choices,
        default=status_choices[0][0]
    )

    def __str__(self):
        return "{id}, {user}, {service}, {total}, {status}".format(
            id=self.id,
            user=self.user.telegram_username,
            service=self.service.name,
            status=self.get_status_display(),
        )