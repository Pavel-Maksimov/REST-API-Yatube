from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Follow, Group, Post, User
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'author__username']

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(following=user)
