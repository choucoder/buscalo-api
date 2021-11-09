from uuid import uuid4

# from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    REGULAR = 2

    telegram_user_id = models.CharField(max_length=150, unique=True, default=str(uuid4()))
    telegram_chat_id = models.CharField(max_length=150, unique=True, default=str(uuid4()))
    telegram_username = models.CharField(max_length=150, unique=True, default=str(uuid4()))

    username = models.CharField(max_length=150, unique=True)

    type_choices = [
        (ADMIN, 'ADMIN'),
        (REGULAR, 'REGULAR'),
    ]

    type = models.PositiveSmallIntegerField(
        default=type_choices[0][0],
        choices=type_choices
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    profile_photo = models.FileField()

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
    )
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email', 'password']


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return "{tg_user_id}, {first_name}, {type}, {is_verified}".format(
            tg_user_id=self.telegram_user_id,
            first_name=self.first_name,
            type=self.type_choices[self.type - 1][1],
            is_verified=self.is_verified
        )


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    created_at = models.DateTimeField(default=timezone.now)


class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=150, default=str(uuid4()))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{user}, {key}, {created_at}".format(
            user=f"{self.user.first_name}, {self.telegram_username}",
            key=self.key,
            created_at=self.created_at
        )


class PushHistories(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amout = models.IntegerField(default=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{user}, {amout}, {created_at}".format(
            user=self.user.first_name,
            amout=self.amout,
            created_at=self.created_at
        )
