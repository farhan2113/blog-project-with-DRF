from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, SignUpApiView, LogInApiView, RefreshAccessTokenApiView, LogOutApiView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpApiView.as_view(), name= 'sign-up'),
    path('login/', LogInApiView.as_view(), name= 'login'),
    path('refresh-access-token/', RefreshAccessTokenApiView.as_view(), name='refresh-access-token'),
    path('logout/', LogOutApiView.as_view(), name='logout'),
]