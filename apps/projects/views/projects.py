"""Project views."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Serializers
from apps.projects.serializers import (
    ProjectModelSerializer,
    ProjectCreateSerializer
)

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.projects import IsProjectOwner, ProjectIsNotFinished

# Models
from apps.projects.models import Project

# Utils
from apps.utils.views import DynamicFieldView


class ProjectViewSet(DynamicFieldView,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Project view set."""

    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()
    lookup_field = 'slug_name'

    # Return dynamic fields
    fields_to_return = {
        'list': ('title', 'slug_name', 'description', 'cost', 'reputation', 'category'),
    }

    def get_permissions(self):
        """Get permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action in ['update', 'finish']:
            permission_classes.extend([IsProjectOwner, ProjectIsNotFinished])
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Handle project creation."""
        serializer = ProjectCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        data = ProjectModelSerializer(project).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def finish(self, request, slug_name):
        """Finish a project."""
        instance = get_object_or_404(Project, slug_name=slug_name)
        serializer = self.get_serializer(instance, data={'finished': True}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
