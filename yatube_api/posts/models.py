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


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
        blank=False,
    )


class Group(models.Model):
    title = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        unique=True,
    )
    description = models.TextField(

    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='group',
        null=True,
    )

    def __str__(self):
        return self.title
