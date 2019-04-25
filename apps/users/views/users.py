"""User views."""

# Django REST Framework
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAccountOwner

# Models
from apps.users.models import User

# Serializers
from apps.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer,
    VerifyAccountSerializer,
    UserLoginSerializer
)

class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """A viewset that provides login, signup and verification account."""

    serializer_class = UserModelSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'


    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve':
            permission_classes.append(IsAuthenticated)
            permission_classes.append(IsAccountOwner)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """Signup action."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'message': 'Now go and verify your account with email.',
            'user': self.get_serializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='verify/(?P<token>[a-zA-Z0-9]+)')
    def verify(self, request, token):
        """Verify accounts."""
        serializer = VerifyAccountSerializer(data={'token':token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations! Now you can login.'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login action."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'token': token,
            'user': self.get_serializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)
