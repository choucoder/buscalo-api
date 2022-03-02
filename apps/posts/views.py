from datetime import datetime

from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.posts.utils import has_text_or_photo, is_allowed_to_post
from .models import Post
from .serializers import CreatePostSerializer, ListPostSerializer
from .permissions import IsPostOwner
from .filters import PostFilter
from apps.products.models import Product
from apps.shops.models import Shop
from apps.products.permissions import IsProductOwner
from users.models import SearchSetting
from core.views import PaginateAPIView


class PostsAPIView(PaginateAPIView):
    serializer_classes = {
        'list': ListPostSerializer,
        'create': CreatePostSerializer
    }
    default_serializer_class = CreatePostSerializer
    permission_classes = (IsPostOwner, )

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)

    def get(self, request):
        user = request.user
        settings = SearchSetting.objects.filter(user=user).first()
        me_location = user.location if not settings.location else settings.location

        if me_location:
            posts = Post.objects.filter(
                location__distance_lt=(
                    me_location,
                    Distance(m=settings.distance)
                )
            )
        else:
            posts = Post.objects.all()

        f = PostFilter(request.GET, queryset=posts)
        page = self.paginate_queryset(f.qs.order_by('-created_at'))
        for post in page:
            if request.user != post.user:
                post.set_view(request.user)

        if page is not None:
            serializer = self.get_serializer_class('list')(page, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        has_text_or_photo(data)
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            is_allowed_to_post(data, request.user)
            user = request.user
            shop = Shop.objects.filter(user=user).first()
            post = serializer.save(user=user, location=user.location, shop=shop)
            user.post_charge(post)
            serializer = self.get_serializer_class('list')(instance=post)
            return Response(
                {"data": serializer.data, "status": status.HTTP_201_CREATED},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )


class PostAPIView(APIView):
    permission_classes = (IsPostOwner, )
    serializer_classes = {
        'list': ListPostSerializer,
        'create': CreatePostSerializer
    }
    default_serializer_class = CreatePostSerializer

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)
        
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer_class('list')(post)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = self.get_serializer_class('create')(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'data': serializer.data}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class MePostsAPIView(APIView):

    serializer_class = CreatePostSerializer
    permission_classes = (IsPostOwner, )

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        serializer = self.serializer_class(instance=posts, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class PostProductsAPIView(APIView):
    serializer_classes = {
        'list': ListPostSerializer,
        'create': CreatePostSerializer
    }
    default_serializer_class = CreatePostSerializer
    permission_classes = (IsProductOwner, )

    def get_serializer_class(self, action):
        return self.serializer_classes.get(action, self.default_serializer_class)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)
        data = request.data
        data['type'] = Post.PRODUCT
        serializer = self.get_serializer_class('create')(data=request.data)

        if serializer.is_valid():
            is_allowed_to_post(request.data, request.user)
            shop = product.shop
            user = request.user
            post = serializer.save(
                user=request.user,
                shop=product.shop,
                product=product,
                location=shop.location if shop.location else user.location
            )
            user = request.user
            user.post_charge(post)
            serializer = self.get_serializer_class('list')(post)
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )