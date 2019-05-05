"""Worker serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Worker

# Choices
from apps.users.choices import POSITION_CHOICES

# Utils
from apps.utils.validators import choices_validator


class WorkerModelSerializer(serializers.ModelSerializer):
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

        # Serializer
        from apps.users.serializers import ProfileWorkerModelSerializer

        return ProfileWorkerModelSerializer(
            obj.worker,
            read_only=True,
            fields=('reputation', 'profile')
        )

    def validate_position(self, value):
        """Show choices."""
        return choices_validator(value, POSITION_CHOICES)
