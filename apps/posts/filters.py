import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['type', 'notify_type']