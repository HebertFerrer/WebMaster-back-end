# """Worker serializers."""

# # Django REST Framework
# from rest_framework import serializers

# # Models
# from apps.projects.models import Worker

# # Choices
# from apps.users.choices import POSITION_CHOICES

# # Utils
# from apps.utils.validators import choices_validator
# from apps.utils.serializers import DynamicFieldsModelSerializer


# class WorkerModelSerializer(DynamicFieldsModelSerializer):
#     """Worker model serializer."""

#     project = serializers.StringRelatedField()

#     # Nested
#     worker = serializers.SerializerMethodField()

#     # choices
#     position = serializers.CharField(source='get_position_display')

#     class Meta:
#         """Meta class."""
#         model = Worker
#         fields = (
#             'id',
#             'worker',
#             'project',
#             'position',
#             'created',
#         )

#     def get_worker(self, obj):
#         """Return worker information."""
#         from apps.users.serializers import UserModelSerializer
#         view = self.context.get('view', None)
#         fields = UserModelSerializer.Meta.fields

#         if view is not None:
#             # Projects
#             if view.view_name == 'projects' and view.action in view.fields_to_return:
#                 fields = view.fields_to_return[view.action]['workers']['worker']

#         if obj.worker:
#             return UserModelSerializer(
#                 obj.worker,
#                 fields=fields,
#                 context=self.context
#             ).data
#         return None

#     def validate_position(self, value):
#         """Show choices."""
#         return choices_validator(value, POSITION_CHOICES)

#     def create(self, data):
#         """Handle creation."""
#         position = data.pop('get_position_display')
#         return Worker.objects.create(
#             project=self.context['project'],
#             position=position
#         )

#     def update(self, instance, data):
#         """Handle update."""
#         position = data.pop('get_position_display')
#         instance.position = position
#         instance.save()
#         return instance
