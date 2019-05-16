"""Califications to creator view."""

# Django REST Framework
from rest_framework import viewsets, status, mixins

# Models
from apps.califications.models import CalificationToCreator

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.califications.permissions import IsWorker

# Serializers
from apps.califications.serializers import CalificationToCreatorModelSerializer

# Utils
from apps.utils.mixins import WorkerDispatchMixin
from apps.utils.views import DynamicFieldView


class CalificationToCreatorViewSet(WorkerDispatchMixin,
                                   DynamicFieldView,
                                   mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """Calification to creator view set."""

    serializer_class = CalificationToCreatorModelSerializer

    # Dynamic fields
    fields_to_return = {
        'list': ('stars', 'comments', '_from',)
    }


    def get_queryset(self):
        """Return queryset."""
        return CalificationToCreator.objects.filter(worker=self.worker)

    def get_serializer_context(self):
        """Add extra context base on action."""
        context = super(CalificationToCreatorViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['worker'] = self.worker
        return context

    def get_permissions(self):
        """Handle permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsWorker)
        return [p() for p in permission_classes]
