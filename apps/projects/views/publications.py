"""Publication views."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

# Serializers
from apps.publications.serializers import (
    PublicationModelSerializer,
    PublicationCreateSerializer
)

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.second_level import IsProjectOwner, ProjectIsNotFinished

# Models
from apps.publications.models import Publication

# Utils
from apps.utils.mixins import ProjectDispatchMixin


class PublicationViewSet(ProjectDispatchMixin,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """Publication view set.

    This handle publication CRUD for project owner.
    """

    serializer_class = PublicationModelSerializer
    # permission_classes = [IsAuthenticated, IsProjectOwner, ProjectIsNotFinished]

    def get_permissions(self):
        """Return permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'delete']:
            permission_classes.extend([IsProjectOwner, ProjectIsNotFinished])
        return [p() for p in permission_classes]

    def get_queryset(self):
        """Return queryset."""
        return Publication.objects.filter(project=self.project)

    def create(self, request, *args, **kwargs):
        """Create publication."""
        serializer = PublicationCreateSerializer(
            data=request.data,
            context={'project': self.project}
        )
        serializer.is_valid(raise_exception=True)
        publication = serializer.save()
        data = self.get_serializer(publication).data
        return Response(data, status=status.HTTP_201_CREATED)
