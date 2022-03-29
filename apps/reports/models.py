from django.db import models

from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

from users.models import User
from apps.posts.models import Post
from apps.products.models import Product


class Report(models.Model):
    type_choices = [
        (1, 'Nudes'),
        (2, 'Violence'),
        (3, 'Suicide'),
        (4, 'Fake information'),
        (5, 'Spam'),
        (6, 'Hate speech'),
        (7, 'Terrorism'),
        (8, 'Other'),
    ]

    issued_choices = [
        (0, 'Post'),
        (1, 'Product')
    ]
    
    id = ShortUUIDField(
        length=32,
        max_length=32,
        primary_key=True,
        editable=False,
        alphabet='0123456789'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    type = models.PositiveSmallIntegerField(
        default=type_choices[0][0],
        choices=type_choices
    )    
    issued_by_model = models.PositiveSmallIntegerField(
        default=issued_choices[0][0],
        choices=issued_choices
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_owner")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reporter")

    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        issued = self.post if self.post else self.product

        return "{issued_id}, {type}, {issued_for}, {reported_by}".format(
            issued=issued.id,
            type=self.type_choices[self.type - 1],
            issued_for=self.issued_choices[self.issued_by_model],
            reported_by=self.reported_by.first_name
        )