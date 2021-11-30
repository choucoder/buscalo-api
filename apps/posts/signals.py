from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, SearchSetting
from .models import Post
from apps.feeds.models import Feed


@receiver(post_save, sender=Post)
def emit_post_to_users(sender, instance, created, **kwargs):
    if created:
        print("emitiendo post a todos los usuarios")
        users = User.objects.all()
        for user in users:
            settings = SearchSetting.objects.get(user=user)
            location = settings.location if settings.location else user.location

            if location and instance.location:
                distance = location.distance(instance.location)
                distance_in_km = distance * 100
                distance_in_mt = distance_in_km * 1000

                if distance_in_mt <= settings.distance:
                    print(f"Usuario {user.first_name} tiene un nuevo post que ver")
                    user_feed = Feed(user=user, post=instance)
                    user_feed.save()
            