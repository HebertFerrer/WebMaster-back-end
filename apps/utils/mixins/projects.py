"""Mixins."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets

# Models
from apps.projects.models import Project


class ProjectDispatchMixin(viewsets.GenericViewSet):
    """Verify that the project exists via dispatch."""

    def dispatch(self, request, *args, **kwargs):
        """Validate project exists."""
        slug_name = kwargs['slug_name']
        self.project = get_object_or_404(Project, slug_name=slug_name)
        return super(ProjectDispatchMixin, self).dispatch(request, *args, **kwargs)

    def get_project(self):
        """Return project in the url."""
        return self.project
