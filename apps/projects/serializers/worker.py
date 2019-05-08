"""Worker serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Worker

# Choices
from apps.users.choices import POSITION_CHOICES

# Utils
from apps.utils.validators import choices_validator
from apps.utils.serializers import DynamicFieldsModelSerializer


class WorkerModelSerializer(DynamicFieldsModelSerializer):
    """Worker model serializer."""

    worker = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""
        model = Worker
        fields = (
            'worker',
            'project',
            'position',
        )

    def get_worker(self, obj):
        """Return worker information."""

        print('Este es el obj: {}'.format(obj.worker))

        # Serializer
        from apps.users.serializers import UserModelSerializer

        return UserModelSerializer(
            obj.worker,
            fields=('username', 'profile_worker')
        ).data

    def validate_position(self, value):
        """Show choices."""
        return choices_validator(value, POSITION_CHOICES)
