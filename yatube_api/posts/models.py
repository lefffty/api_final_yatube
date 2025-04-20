from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        blank=False,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group', on_delete=models.SET_NULL, related_name='posts',
        null=True, blank=True,
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(
        blank=False,
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Group(models.Model):
    title = models.CharField(
        verbose_name='Название группы',
        max_length=30,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг группы',
    )
    description = models.TextField(
        verbose_name='Описание группы',
    )

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        # ограничение на уникальность подписки
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow',
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
