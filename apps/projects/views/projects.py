"""Project views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response


# Serializers
from apps.projects.serializers import (
    ProjectModelSerializer,
    ProjectCreateSerializer
)

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from apps.projects.models import Project


class ProjectViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """Project view set."""

    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()
    lookup_field = 'slug_name'


    def get_permissions(self):
        """Get permissions base on action."""
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Handle project creation."""
        serializer = ProjectCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        data = ProjectModelSerializer(project).data
        return Response(data, status=status.HTTP_201_CREATED)
