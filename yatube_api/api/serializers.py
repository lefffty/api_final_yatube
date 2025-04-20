from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model


from posts.models import (
    Comment,
    Post,
    Group,
    Follow,
)

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post', )
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = (
            'user',
            'following',
        )
        model = Follow

    def validate_following(self, value):
        """
        Нелья подписаться на самого себя
        """
        request_user = self.context['request'].user
        if request_user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value

    def validate(self, attrs):
        """
        Нельзя подписаться на одного пользователя дважды
        """
        user = self.context['request'].user
        if Follow.objects.filter(user=user, following=attrs['following']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return attrs

    def create(self, validated_data):
        """
        Создание подписки
        """
        return Follow.objects.create(
            user=self.context['request'].user,
            following=validated_data['following'],
        )
