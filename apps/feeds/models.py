from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from shortuuid.django_fields import ShortUUIDField

from users.models import User
from apps.posts.models import Post


class Feed(models.Model):
    id = ShortUUIDField(
        length=24,
        max_length=32,
        primary_key=True,
        editable=False,
        alphabet='0123456789abcdefghijklmnopqrstuvwxyz'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def mark_as_seen(self):
        self.seen = True
        super().save()

    def expired(self):
        pass

    def __str__(self):
        return "{user}, {post}, {seen}".format(
            user=self.user.first_name,
            post=self.post.title,
            seen=self.seen
        )
