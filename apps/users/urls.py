"""User urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework import routers

# Views
from apps.users.views import users as user_views


router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
