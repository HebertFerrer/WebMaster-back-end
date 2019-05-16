"""Califications permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from apps.projects.models import Project


class IsBoss(BasePermission):
    """Return permissions."""

    def has_permission(self, request, view):
        """Handle validation.

        Ensures that the request user is worker's boss from a finished project.
        """
        worker_user = view.get_worker().profile.user
        queryset = Project.objects.filter(
            workers=worker_user,
            finished=True
        ).values_list('creator')
        creator_list = [item[0] for item in queryset]
        return request.user.pk in creator_list


class IsWorker(BasePermission):
    """Return permissions."""

    def has_permission(self, request, view):
        """Return validation.

        Ensures that the request user is creator's worker from a finished project.
        """
        creator_user = view.get_creator().profile.user
        queryset = Project.objects.filter(
            creator=creator_user,
            finished=True
        ).values_list('workers')
        worker_list = [item[0] for item in queryset]
        return request.user.pk in worker_list


class IsNotProjectOwner(BasePermission):
    """Return permissions."""

    def has_permission(self, request, view):
        """Return validation."""
        project = view.get_project()
        return request.user != project.creator and project.finished
