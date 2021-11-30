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
