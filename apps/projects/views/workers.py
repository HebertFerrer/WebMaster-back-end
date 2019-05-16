"""Worker views."""

# Django REST Framework
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from apps.projects.models import Worker

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.second_level import (
    IsProjectOwner,
    IsNotProjectOwner,
    ProjectIsNotFinished
)

# Serializers
from apps.projects.serializers import WorkerModelSerializer
from apps.projects.serializers import (
    ApplicationModelSerializer,
    ApplicationCreateSerializer,
)

# Utils
from apps.utils.mixins import ProjectDispatchMixin


class WorkerViewSet(ProjectDispatchMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Worker view set."""

    serializer_class = WorkerModelSerializer

    def get_queryset(self):
        return Worker.objects.filter(project=self.project)

    def get_serializer_context(self):
        """Handle serializer context base on action."""
        context = super(WorkerViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['project'] = self.project
        return context

    def get_permissions(self):
        """Get permissions base on actions."""
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update']:
            permission_classes.extend([IsProjectOwner, ProjectIsNotFinished])
        if self.action == 'applicate':
            permission_classes.extend([IsNotProjectOwner, ProjectIsNotFinished])
        return [p() for p in permission_classes]

    @action(detail=True, methods=['post'])
    def applicate(self, request, slug_name, pk):
        """Handle request to a specific job in a project."""
        context = {'request': request, 'job_pk': pk}
        serializer = ApplicationCreateSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        data = ApplicationModelSerializer(application).data
        return Response(data, status=status.HTTP_201_CREATED)
