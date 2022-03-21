from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, SearchSetting
from .models import Post
from apps.feeds.models import Feed


@receiver(post_save, sender=Post)
def emit_post_to_users(sender, instance, created, **kwargs):
    if created:
        pass