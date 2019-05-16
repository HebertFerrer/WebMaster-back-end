"""Project permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    """Check if request.user is project owner."""

    def has_permission(self, request, view):
        """Check permissions."""
        return request.user == view.get_object().creator


class ProjectIsNotFinished(BaseException):
    """Check if project is not finished."""

    def has_permission(self, request, view):
        """Check permissions."""
        return not view.get_object().finished


class ProjectIsFinished(BaseException):
    """Check if project is finished."""

    def has_permission(self, request, view):
        """Check permissions."""
        return view.get_object().finished
