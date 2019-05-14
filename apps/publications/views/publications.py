"""Publication views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from apps.publications.models import Publication

# Serializers
from apps.publications.serializers import PublicationModelSerializer


class PublicationViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Publication view set.

    This handle publication actions from users that aren't
    project owners.
    """

    serializer_class = PublicationModelSerializer
    queryset = Publication.objects.all()
    permission_classes = [IsAuthenticated]
