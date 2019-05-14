"""Likes view."""

# Django REST Framework
from rest_framework import viewsets, mixins, status

# Models
from apps.publications.models import Publication, Like

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.publications.permissions import IsComment_LikeOwner

# Serializers
from apps.publications.serializers import LikeModelSerializer

# Utils
from apps.utils.mixins import PublicationDispatchMixin
from apps.utils.views import DynamicFieldView


class LikeViewSet(PublicationDispatchMixin,
                  DynamicFieldView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Generic view set."""

    serializer_class = LikeModelSerializer

    # Return dynamic fields
    fields_to_return = {
        'list': ('id', 'user',)
    }

    def get_queryset(self):
        """Return queryset."""
        return Like.objects.filter(publication=self.publication)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            permission_classes.append(IsComment_LikeOwner)
        return [p() for p in permission_classes]

    def get_serializer_context(self):
        """Return serializer context."""
        context = super(LikeViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['publication'] = self.publication
        return context
