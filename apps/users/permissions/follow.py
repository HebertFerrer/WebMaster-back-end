"""Follow permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Verify if the user is account owner."""

    def has_permission(self, request, view):
        """Verify if the request..user is the same as view.obj"""
        return request.user == view.get_user()


class IsNotAccountOwner(BasePermission):
    """Verify if the user isn't account owner."""

    def has_permission(self, request, view):
        """Validates that an user can't follow himself."""
        return request.user != view.get_user()
