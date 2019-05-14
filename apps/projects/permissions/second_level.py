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

