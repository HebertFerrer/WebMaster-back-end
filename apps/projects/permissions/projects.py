"""Project permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    """Check if request.user is project owner."""

    def has_permission(self, request, view):
        """Validates if request.user == project creator."""
        return request.user == view.get_object().creator
