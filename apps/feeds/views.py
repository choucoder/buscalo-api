from random import randint
from django.contrib.gis.measure import Distance
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Feed
from .serializers import FeedSerializer
from core.views import PaginateAPIView
from users.models import SearchSetting
from apps.posts.models import Post


class FeedsAPIView(PaginateAPIView):
    serializer_class = FeedSerializer

    def get(self, request):
        user = request.user
        settings = SearchSetting.objects.filter(user=user).first()
        user_location = settings.location if not user.location else user.location

        feed = None
        feed_radius = 250 * 1000

        if user_location:
            posts = Post.objects.filter(
                location__distance_lt=(
                    user_location,
                    Distance(m=feed_radius)
                )
            ).order_by('-created_at').values_list('id', flat=True)

            seen_posts = Feed.objects.filter(user=user).order_by('-created_at').values_list('post', flat=True)
            unseen_posts = posts.difference(seen_posts)

            if unseen_posts:
                unseen_post = Post.objects.filter(id__in=unseen_posts).annotate(distance=Distance('location', user_location)).order_by('-created_at', 'distance').first()
                unseen_post.views += 1
                unseen_post.save()
                # Mark post as viewed
                unseen_feed = Feed(user=user, post=unseen_post, views=1)
                unseen_feed.save()
                feed = unseen_feed
            else:
                seen_posts = Feed.objects.filter(user=user).order_by('views', 'created_at')
                if seen_posts:
                    i = randint(0, seen_posts.count() - 1)
                    seen_feed = seen_posts[i]
                    seen_feed.views += 1
                    seen_feed.save()
                    feed = seen_feed

        else:
            posts = Post.objects.filter().order_by('-created_at').values_list('id', flat=True)
            seen_posts = Feed.objects.filter(user=user).order_by('-created_at').values_list('post', flat=True)
            unseen_posts = posts.difference(seen_posts)

            if unseen_posts:
                unseen_post = Post.objects.filter(id__in=unseen_posts).order_by('-created_at').first()
                unseen_post.views += 1
                unseen_post.save()
                # Mark post as viewed
                unseen_feed = Feed(user=user, post=unseen_post, views=1)
                unseen_feed.save()
                feed = unseen_feed
            else:
                seen_posts = Feed.objects.filter(user=user).order_by('views', 'created_at')
                if seen_posts:
                    i = randint(0, seen_posts.count() - 1)
                    seen_feed = seen_posts[i]
                    seen_feed.views += 1
                    seen_feed.save()
                    feed = seen_feed

        if feed:
            serializer = self.serializer_class(instance=feed)
            return Response({
                'data': [serializer.data],
            }, status=status.HTTP_200_OK)
        else:
            return Response({'data': []}, status=status.HTTP_200_OK)


class FeedsOldAPIView(PaginateAPIView):

    serializer_class = FeedSerializer

    def get(self, request):
        user = request.user
        settings = SearchSetting.objects.filter(user=user).first()
        me_location = user.location if not settings.location else settings.location

        if me_location:
            feeds = Feed.objects.filter(
                post__location__distance_lt=(
                    me_location,
                    Distance(m=settings.distance)
                ),
                post__notify_type=Post.PUSH,
                user=user,
                seen=False
            ).order_by('created_at')

            if not feeds:
                feeds = Feed.objects.filter(
                    post__location__distance_lt=(
                        me_location,
                        Distance(m=settings.distance)
                    ),
                    user=user,
                    seen=False
                ).order_by('created_at')

        else:
            feeds = Feed.objects.filter(user=user, seen=False)
            if not feeds:
                feeds = Feed.objects.filter(
                    user=user,
                    seen=False,
                    post__notify_type=Post.PUSH
                )
        page = self.paginate_queryset(feeds)

        for feed in page:
            feed.mark_as_seen()
            feed.post.set_view(request)
        
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
