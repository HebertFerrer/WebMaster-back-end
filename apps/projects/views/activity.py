"""Activirty views."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets, mixins, status

# Serializers
from apps.projects.serializers import ActivityModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.activity import IsProjectOwner

# Models
from apps.projects.models import Activity, Project


class ActivityViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Activity view set."""

    serializer_class = ActivityModelSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsProjectOwner)
        return [p() for p in permission_classes]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the project exists."""
        slug_name = kwargs['slug_name']
        self.project = get_object_or_404(Project, slug_name=slug_name)
        return super(ActivityViewSet, self).dispatch(request, *args, **kwargs)

    def get_project(self):
        """Return project in the url."""
        return self.project

