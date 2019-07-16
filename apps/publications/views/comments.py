"""Comments view."""

# Django REST Framework
from rest_framework import viewsets, mixins, status

# Models
from apps.publications.models import Publication, Comment

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.publications.permissions import IsCommentOwner, IsPublicationOwner

# Serializers
from apps.publications.serializers import CommentModelSerializer

# Utils
from apps.utils.mixins import PublicationDispatchMixin


class CommentViewSet(PublicationDispatchMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """Comment view set."""

    serializer_class = CommentModelSerializer


    def get_serializer_context(self):
        """Return context base on action."""
        context = super(CommentViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['publication'] = self.publication
        return context

    def get_permissions(self):
        """Handle permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action == 'update':
            permission_classes.append(IsCommentOwner)
        if self.action == 'delete':
            permission_classes.extend([IsCommentOwner, IsPublicationOwner])
        return [p() for p in permission_classes]

    def get_queryset(self):
        """Return queryset."""
        return Comment.objects.filter(publication=self.publication)
