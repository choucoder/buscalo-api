
from geopy.geocoders import Nominatim
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from core.utils import get_filename, generate_random_uuid, clean_str
from core.models import Address


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    REGULAR = 2

    id = ShortUUIDField(
        length=16,
        max_length=32,
        primary_key=True,
        editable=False,
        alphabet='0123456789'
    )

    telegram_user_id = models.CharField(
        max_length=150, unique=True, default=generate_random_uuid
    )
    telegram_chat_id = models.CharField(
        max_length=150, unique=True, default=generate_random_uuid
    )
    telegram_username = models.CharField(
        max_length=150, unique=True, default=generate_random_uuid
    )

    username = models.CharField(max_length=150, unique=True)

    type_choices = [
        (ADMIN, 'ADMIN'),
        (REGULAR, 'REGULAR'),
    ]

    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    type = models.PositiveSmallIntegerField(
        default=type_choices[0][0],
        choices=type_choices
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=16, choices=gender_choices, default=gender_choices[2][0])
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to=get_filename, blank=True, null=True)
    
    location = models.PointField(geography=True, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    
    push_post_amount = models.IntegerField(default=2)
    
    is_staff = models.BooleanField(
        default=True,
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

    def post_charge(self, post):
        if post.notify_type == 1:
            self.push_post_amount -= 1
            super().save()

    def update_address(self, is_location=True):
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
            except:
                pass

    def __str__(self):
        return "{tg_user_id}, {first_name}, {type}, {is_verified}".format(
            tg_user_id=self.telegram_user_id,
            first_name=self.first_name,
            type=self.get_type_display(),
            is_verified=self.is_verified
        )


class UserVerification(models.Model):
    key = ShortUUIDField(
        length=22,
        max_length=40,
        unique=True,
        editable=False,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{user}, {key}, {created_at}".format(
            user=f"{self.user.first_name}, {self.telegram_username}",
            key=self.key,
            created_at=self.created_at
        )


class SearchSetting(models.Model):
    id = ShortUUIDField(
        length=16,
        max_length=32,
        unique=True,
        editable=False,
        alphabet='0123456789',
        primary_key=True,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.PointField(geography=True, blank=True, null=True)
    distance = models.IntegerField(default=5000)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{user}, {location}, {distance}".format(
            user=f"{self.user.first_name}, {self.telegram_username}",
            key=self.location,
            created_at=self.distance
        )