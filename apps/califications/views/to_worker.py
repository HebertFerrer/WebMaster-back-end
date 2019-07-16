# """Califications to worker view."""

# # Django REST Framework
# from rest_framework import viewsets, status, mixins

# # Models
# from apps.califications.models import CalificationToWorker

# # Permissions
# from rest_framework.permissions import IsAuthenticated
# from apps.califications.permissions import IsBoss

# # Serializers
# from apps.califications.serializers import CalificationToWorkerModelSerializer

# # Utils
# from apps.utils.mixins import WorkerDispatchMixin
# from apps.utils.views import DynamicFieldView


# class CalificationToWorkerViewSet(WorkerDispatchMixin,
#                                   DynamicFieldView,
#                                   mixins.ListModelMixin,
#                                   mixins.CreateModelMixin,
#                                   viewsets.GenericViewSet):
#     """Calification to worker view set."""

#     serializer_class = CalificationToWorkerModelSerializer

#     # Dynamic fields
#     fields_to_return = {
#         'list': ('stars', 'comments', '_from',)
#     }


#     def get_queryset(self):
#         """Return queryset."""
#         return CalificationToWorker.objects.filter(worker=self.worker)

#     def get_serializer_context(self):
#         """Add extra context base on action."""
#         context = super(CalificationToWorkerViewSet, self).get_serializer_context()
#         if self.action == 'create':
#             context['worker'] = self.worker
#         return context

#     def get_permissions(self):
#         """Handle permissions base on action."""
#         permission_classes = [IsAuthenticated]
#         if self.action == 'create':
#             permission_classes.append(IsBoss)
#         return [p() for p in permission_classes]
