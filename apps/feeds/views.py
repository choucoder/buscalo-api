from random import randint
from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404
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


class FeedAPIView(APIView):

    serializer_class = FeedSerializer

    def get(self, request, pk):
        feed = get_object_or_404(Feed, pk=pk)

        serializer = self.serializer_class(instance=feed)
        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)