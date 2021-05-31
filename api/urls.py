from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowList, GroupList, PostViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('v1/', include(router_v1.urls)),
    path('v1/follow/', FollowList.as_view(), name='follow'),
    path('v1/group/', GroupList.as_view(), name='group'),
]
