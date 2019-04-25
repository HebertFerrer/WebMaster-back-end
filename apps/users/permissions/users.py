"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Verify if the user is account owner."""

    def has_object_permission(self, request, view, obj):
        """Verify if request.user is the same as obj."""
        return request.user == obj
