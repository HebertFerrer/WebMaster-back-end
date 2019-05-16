"""Activity permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    """Check if the request user is the project creator."""

    def has_permission(self, request, view):
        """Check permissions."""
        return request.user == view.get_project().creator


class IsNotProjectOwner(BasePermission):
    """Check if the request user is the project creator."""

    def has_permission(self, request, view):
        """Check permissions."""
        return request.user != view.get_project().creator


class ProjectIsNotFinished(BaseException):
    """Check if project is not finished."""

    def has_permission(self, request, view):
        """Check permisions."""
        return not view.get_project().finished


class ProjectIsFinished(BaseException):
    """Check if project is finished."""

    def has_permission(self, request, view):
        """Check permisions."""
        return view.get_project().finished
