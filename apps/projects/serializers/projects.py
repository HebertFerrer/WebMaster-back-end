"""Project serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Project, Worker

# Choices
from apps.projects.choices import CATEGORY_CHOICES

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer
from apps.utils.validators import choices_validator

# Serializer
from apps.projects.serializers.worker import WorkerModelSerializer

class ProjectModelSerializer(DynamicFieldsModelSerializer):
    """Project model serializer."""

    workers = serializers.SerializerMethodField()
    slots = serializers.SerializerMethodField()

    # choices
    category = serializers.CharField(source='get_category_display')


    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'title',
            'slug_name',
            'description',
            'cost',
            'reputation',
            'category',
            'creator',
            'workers',
            'slots',
            # 'activities',
        )
        read_only_fields = (
            'reputation',
            'creator',
            'workers',
            # 'activities',
        )

    def get_workers(self, obj):
        """Return users that works in the project."""

        # Serializer
        from apps.projects.serializers import WorkerModelSerializer

        return WorkerModelSerializer(
            Worker.objects.filter(worker__isnull=False, project=obj),
            read_only=True,
            many=True
        )

    def get_slots(self, obj):
        """Handle slots for workers."""

        # Serializer
        from apps.projects.serializers import WorkerModelSerializer

        return WorkerModelSerializer(
            Worker.objects.filter(worker__isnull=True, project=obj),
            many=True
        )


class ProjectCreateSerializer(serializers.Serializer):
    """Handle project creation."""

    title = serializers.CharField(max_length=50)
    slug_name = serializers.SlugField(max_length=8)
    description = serializers.CharField()

    cost = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0
    )

    category = serializers.IntegerField()
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    slots = WorkerModelSerializer(many=True, required=False)

    def validate_category(self, value):
        """Show choices."""
        return choices_validator(value, CATEGORY_CHOICES)
