from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
)
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)
from posts.models import (
    Post,
    Comment,
    Group,
    Follow,
)


@api_view(['GET', 'POST'])
def api_posts(request: HttpRequest):
    if request.user.is_anonymous:
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
    elif request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'POST':
        serializer = PostSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_post(request: HttpRequest, id):
    if request.user.is_anonymous:
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
    post = get_object_or_404(
        Post,
        pk=id,
    )
    if request.user != post.author:
        return Response(
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == 'GET':
        serializer = PostSerializer(
            post,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == 'DELETE':
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET', 'POST'])
def api_comments(request: HttpRequest, post_id):
    comments = Comment.objects.filter(
        post_id__exact=post_id,
    )
    if request.method == 'GET':
        serializer = CommentSerializer(
            comments,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'POST':
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = CommentSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comment(request: HttpRequest, post_id, id):
    comment = get_object_or_404(
        Comment,
        pk=id,
    )
    if request.user.is_anonymous:
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if request.user != comment.author:
        return Response(
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == 'GET':
        serializer = CommentSerializer(
            comment,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
            )
    elif request.method == 'DELETE':
        comment.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET'])
def api_groups(request: HttpRequest):
    groups = Group.objects.all()
    serializer = GroupSerializer(
        groups,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
def api_group(request: HttpRequest, id):
    group = get_object_or_404(
        Group,
        pk=id,
    )
    serializer = GroupSerializer(
        group,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'POST'])
def api_fellow(request: HttpRequest):
    if request.user.is_anonymous:
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if request.method == 'GET':
        if request.user.is_authenticated is False:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        followings = Follow.objects.filter(
            user=request.user,
        )
        serializer = FollowSerializer(
            followings,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'POST':
        serializer = FollowSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
