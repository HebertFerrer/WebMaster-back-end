"""Publication views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from apps.publications.models import Publication
from apps.users.models import Follow, User

# Serializers
from apps.publications.serializers import PublicationModelSerializer


class PublicationViewSet(mixins.ListModelMixin,
                         #  mixins.UpdateModelMixin,
                         #  mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """Publication view set.

    This handle publication actions from users that aren't
    project owners.
    """

    serializer_class = PublicationModelSerializer
    # queryset = Publication.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return queryset."""
        ACTIVE = 1

        inner_followeds = Follow.objects.filter(
            follower=self.request.user, status=ACTIVE
        ).values('followed__username')
        inner_users = User.objects.filter(username__in=inner_followeds)

        return Publication.objects.filter(
            project__creator__in=inner_users
        )
