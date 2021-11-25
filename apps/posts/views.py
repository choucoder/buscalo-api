from django.conf import settings
from django.core.paginator import Page
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.posts.utils import has_text_or_photo, is_allowed_to_post
from apps.products.serializers import CreateProductSerializer

from .models import Post
from .serializers import CreatePostSerializer, ListPostSerializer
from .permissions import IsPostOwner
from .filters import PostFilter
from apps.products.models import Product
from apps.products.permissions import IsProductOwner
from users.models import User
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
        # Los post se ordenaran de acuerdo al rango de distancia
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
        """
        Formulario para crear un post
        1) Postear => Historia, Producto
        2) Historia => Seleccione texto, seleccione imagen
        3) Producto => Tienda => Buscar Producto (Seleccionar todos)
        4) Postear
        Los posts se hacen tambien con una imagen
        Postear una historia (texto, foto)
        """
        data = request.data
        has_text_or_photo(data)
        serializer = self.get_serializer_class('create')(data=data)

        if serializer.is_valid():
            is_allowed_to_post(data, request.user)
            post = serializer.save(user=request.user)
            user = request.user
            user.post_charge(post)
            return Response(
                {"data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"data": serializer.errors},
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


class MePostAPIView(APIView):

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
            post = serializer.save(
                user=request.user,
                shop=product.shop,
                product=product
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