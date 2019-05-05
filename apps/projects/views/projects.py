"""Project views."""

# Django REST Framework
from rest_framework import mixins, viewsets

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
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """Project view set."""

    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()
    lookup_field = 'slug_name'


    def get_permissions(self):
        """Get permissions base on action."""
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        """Get serializer base on action."""
        serializer_class = ProjectModelSerializer
        if self.action == 'create':
            serializer_class = ProjectCreateSerializer
        return serializer_class
