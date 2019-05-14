"""Comment permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsComment_LikeOwner(BasePermission):
    """Validate if the request user is the comment owner."""

    def has_permission(self, request, view):
        """Return permission."""
        return request.user == view.get_object().user
