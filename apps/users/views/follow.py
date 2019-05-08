"""Follow views."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions
from apps.users.permissions.follow import IsAccountOwner, IsNotAccountOwner
from rest_framework.permissions import IsAuthenticated


# Models
from apps.users.models import Follow, User

# Serializer
from apps.users.serializers import (
    FollowModelSerializer,
    FollowCreateSerializer,
    FollowAcceptSerializer,
)


class FollowViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Follow view set."""

    serializer_class = FollowModelSerializer
    lookup_field = 'code'


    def get_queryset(self):
        return Follow.objects.filter(followed=self.user)

    def get_permissions(self):
        """Handle permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsNotAccountOwner)
        if self.action in ['requests', 'accept', 'reject']:
            permission_classes.append(IsAccountOwner)
        return [p() for p in permission_classes]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(FollowViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Handle follow request creation."""
        user = get_object_or_404(User, username=kwargs['username'])
        context = {'request': request, 'user': user}

        serializer = FollowCreateSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        follow = serializer.save()
        data = FollowModelSerializer(follow).data
        return Response(data, status=status.HTTP_201_CREATED)

    def get_user(self):
        """Return url user."""
        return self.user

    # Actions
    @action(detail=False, methods=['get'])
    def requests(self, request, username):
        """List follow request sended."""
        queryset = Follow.objects.filter(followed=self.user, status=3)
        data = FollowModelSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def followers(self, request, username):
        """List followers."""
        queryset = Follow.objects.filter(followed=self.user, status=1)
        data = FollowModelSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def accept(self, request, username, code):
        """Accept follow invitation."""
        follow_request = get_object_or_404(Follow, code=code, followed=self.user)
        serializer = FollowAcceptSerializer(follow_request, data=request.data)
        serializer.is_valid(raise_exception=True)
        follow = serializer.save()
        data = self.get_serializer(follow).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def reject(self, request, username, code):
        """Accept follow invitation."""
        follow_request = get_object_or_404(Follow, code=code, followed=self.user)
        serializer = FollowAcceptSerializer(follow_request, data=request.data)
        serializer.is_valid(raise_exception=True)
        follow = serializer.save()
        data = self.get_serializer(follow).data
        return Response(data, status=status.HTTP_200_OK)
