"""Publication mixins."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets

# Models
from apps.publications.models import Publication

class PublicationDispatchMixin(viewsets.GenericViewSet):
    """Ensures we have a publication in the url."""

    def dispatch(self, request, *args, **kwargs):
        """Validates publication in the url."""
        pk = kwargs['id']
        self.publication = get_object_or_404(Publication, pk=pk)
        return super(PublicationDispatchMixin, self).dispatch(request, *args, **kwargs)

    def get_publication(self):
        """Return publication in the url."""
        return self.publication
