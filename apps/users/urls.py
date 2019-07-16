"""User urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework import routers

# Views
from apps.users.views import users as user_views
from apps.users.views import follow as follow_views


router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
router.register(
    r'users/(?P<username>[a-zA-Z0-9-_@]+)/follow',
    follow_views.FollowViewSet,
    basename='follow'
)

urlpatterns = [
    path('', include(router.urls))
]
