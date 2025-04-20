from rest_framework import viewsets, mixins, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404


from .permissions import (
    OwnerOrReadOnly,
    ReadOnly
)
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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(), )
        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny, )


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, )

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(), )
        return super().get_permissions()

# @api_view(['GET', 'POST'])
# def api_posts(request: HttpRequest):
#     if request.method == 'GET':
#         if request.user.is_anonymous:
#             return Response(
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts,
#             many=True,
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'POST':
#         if request.user.is_authenticated:
#             serializer = PostSerializer(
#                 data=request.data,
#             )
#             if serializer.is_valid():
#                 serializer.validated_data['author'] = request.user
#                 serializer.save()
#                 return Response(
#                     serializer.data,
#                     status=status.HTTP_201_CREATED,
#                 )
#             else:
#                 return Response(
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         else:
#             return Response(
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_post(request: HttpRequest, id):
#     if request.user.is_anonymous:
#         return Response(
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     post = get_object_or_404(
#         Post,
#         pk=id,
#     )
#     if request.method == 'GET':
#         serializer = PostSerializer(
#             post,
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'PUT' or request.method == 'PATCH':
#         if request.user != post.author:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         serializer = PostSerializer(
#             post,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#     elif request.method == 'DELETE':
#         if request.user != post.author:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         post.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT,
#         )


# @api_view(['GET', 'POST'])
# def api_comments(request: HttpRequest, post_id):
#     comments = Comment.objects.filter(
#         post_id__exact=post_id,
#     )
#     if request.method == 'GET':
#         serializer = CommentSerializer(
#             comments,
#             many=True,
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'POST':
#         if request.user.is_anonymous:
#             return Response(
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         serializer = CommentSerializer(
#             data=request.data,
#         )
#         if serializer.is_valid():
#             serializer.validated_data['author'] = request.user
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED,
#             )


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_comment(request: HttpRequest, post_id, id):
#     comment = get_object_or_404(
#         Comment,
#         pk=id,
#     )
#     if request.user.is_anonymous:
#         return Response(
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     if request.method == 'GET':
#         serializer = CommentSerializer(
#             comment,
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'PUT' or request.method == 'PATCH':
#         if request.user != comment.author:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         serializer = CommentSerializer(
#             comment,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 status=status.HTTP_200_OK,
#             )
#     elif request.method == 'DELETE':
#         if request.user != comment.author:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         comment.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT,
#         )


# @api_view(['GET'])
# def api_groups(request: HttpRequest):
#     groups = Group.objects.all()
#     serializer = GroupSerializer(
#         groups,
#         many=True,
#     )
#     return Response(
#         serializer.data,
#         status=status.HTTP_200_OK,
#     )


# @api_view(['GET'])
# def api_group(request: HttpRequest, id):
#     if request.method == 'GET':
#         group = get_object_or_404(
#             Group,
#             pk=id,
#         )
#         serializer = GroupSerializer(
#             group,
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )


# @api_view(['GET', 'POST'])
# def api_fellow(request: HttpRequest):
#     if request.user.is_anonymous:
#         return Response(
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     if request.method == 'GET':
#         if request.user.is_authenticated is False:
#             return Response(
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         followings = Follow.objects.filter(
#             user=request.user,
#         )
#         serializer = FollowSerializer(
#             followings,
#             many=True,
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'POST':
#         if request.user.is_authenticated is False:
#             return Response(
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         serializer = FollowSerializer(
#             data=request.data,
#         )
#         if serializer.is_valid():
#             serializer.validated_data['author'] = request.user
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED,
#             )
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
