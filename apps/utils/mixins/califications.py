"""Califications mixins."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets

# Models
from apps.users.models import (
    # ProfileWorker,
    ProfileCreator
)


# class WorkerDispatchMixin(viewsets.GenericViewSet):
#     """Ensures we have a Worker in the url."""

#     def dispatch(self, request, *args, **kwargs):
#         """Validates worker in the url."""
#         pk = kwargs['id']
#         self.worker = get_object_or_404(ProfileWorker, pk=pk)
#         return super(WorkerDispatchMixin, self).dispatch(request, *args, **kwargs)

#     def get_worker(self):
#         """Return worker in the url."""
#         return self.worker


class CreatorDispatchMixin(viewsets.GenericViewSet):
    """Ensures we have a Creator in the url."""

    def dispatch(self, request, *args, **kwargs):
        """Validates creator in the url."""
        pk = kwargs['id']
        self.creator = get_object_or_404(ProfileCreator, pk=pk)
        return super(CreatorDispatchMixin, self).dispatch(request, *args, **kwargs)

    def get_creator(self):
        """Return creator in the url."""
        return self.creator
