from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title']
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if data.get('following') == data.get('user'):
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя.'
            )
        return data

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Подписка уже оформлена.'
            )
        ]
