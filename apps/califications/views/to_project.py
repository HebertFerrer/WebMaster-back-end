"""Califications to project view."""

# Django REST Framework
from rest_framework import viewsets, status, mixins

# Models
from apps.califications.models import CalificationToProject

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.califications.permissions import IsNotProjectOwner

# Serializers
from apps.califications.serializers import CalificationToProjectModelSerializer

# Utils
from apps.utils.mixins import ProjectDispatchMixin
from apps.utils.views import DynamicFieldView


class CalificationToProjectViewSet(ProjectDispatchMixin,
                                   DynamicFieldView,
                                   mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """Calification to worker view set."""

    serializer_class = CalificationToProjectModelSerializer

    # Dynamic fields
    fields_to_return = {
        'list': ('stars', 'comments', '_from',)
    }


    def get_queryset(self):
        """Return queryset."""
        return CalificationToProject.objects.filter(project=self.project)

    def get_serializer_context(self):
        """Add extra context base on action."""
        context = super(CalificationToProjectViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['project'] = self.project
        return context

    def get_permissions(self):
        """Handle permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsNotProjectOwner)
        return [p() for p in permission_classes]
