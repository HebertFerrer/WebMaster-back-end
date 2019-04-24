"""User views."""

# Django REST Framework
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from apps.users.models import User

# Serializers
from apps.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer,
)

class UserViewSet(viewsets.GenericViewSet):
    """A viewset that provides login, signup and verification account."""

    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """Signup action."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = self.get_serializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
