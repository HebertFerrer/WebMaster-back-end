"""Publication permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsPublicationOwner(BasePermission):
    """Validate if the user request is the publication owner."""

    def has_permission(self, request, view):
        """Return permission."""
        return request.user == view.get_publication().project.creator
