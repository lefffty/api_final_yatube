from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'follow', views.FollowViewSet)
router.register(r'posts\/(?P<post_id>\d+)\/comments', views.CommentViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    # path(
    #     'v1/posts/',
    #     views.api_posts,
    # ),
    # path(
    #     'v1/posts/<int:id>/',
    #     views.api_post,
    # ),
    # path(
    #     'v1/posts/<int:post_id>/comments/',
    #     views.api_comments,
    # ),
    # path(
    #     'v1/posts/<int:post_id>/comments/<int:id>/',
    #     views.api_comment,
    # ),
    # path(
    #     'v1/groups/',
    #     views.api_groups,
    # ),
    # path(
    #     'v1/groups/<int:id>/',
    #     views.api_group,
    # ),
    # path(
    #     'v1/follow/',
    #     views.api_fellow,
    # ),
]
