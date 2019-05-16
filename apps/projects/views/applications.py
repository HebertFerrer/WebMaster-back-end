"""Application views."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from apps.projects.models import Application

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.second_level import IsProjectOwner, ProjectIsNotFinished

# Serializers
from apps.projects.serializers import (
    ApplicationModelSerializer,
    ApplicationRejectSerializer,
    ApplicationAcceptSerializer,
)

# Utils
from apps.utils.mixins import ProjectDispatchMixin


class ApplicationViewSet(ProjectDispatchMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Application view set."""

    serializer_class = ApplicationModelSerializer
    lookup_field = 'code'


    def get_queryset(self):
        """Return queyset."""
        return Application.objects.filter(job__project=self.project, status=3)

    def get_permissions(self):
        """Get permissions base on actions."""
        permission_classes = [IsAuthenticated, IsProjectOwner]
        if self.action in ['reject', 'accept']:
            permission_classes.append(ProjectIsNotFinished)
        return [p() for p in permission_classes]

    def get_serializer_context(self):
        """Return context."""
        context = super(ApplicationViewSet, self).get_serializer_context()
        if self.action == 'list':
            context['action'] = self.action
        return context

    @action(detail=True, methods=['put', 'patch'])
    def reject(self, request, slug_name, code):
        """Reject application request."""
        application_request = get_object_or_404(Application, code=code)
        serializer = ApplicationRejectSerializer(application_request, data=request.data)
        serializer.is_valid()
        application = serializer.save()
        data = ApplicationModelSerializer(application).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def accept(self, request, slug_name, code):
        """Reject application request."""
        application_request = get_object_or_404(Application, code=code)
        serializer = ApplicationAcceptSerializer(application_request, data=request.data)
        serializer.is_valid()
        application = serializer.save()
        data = ApplicationModelSerializer(application).data
        return Response(data, status=status.HTTP_200_OK)
