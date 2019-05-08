"""Project serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Project, Worker, Activity

# Choices
from apps.projects.choices import CATEGORY_CHOICES

# Serializer
from apps.projects.serializers.worker import WorkerModelSerializer
from apps.projects.serializers.activity import ActivityModelSerializer

# Validators
from rest_framework.validators import UniqueValidator

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer
from apps.utils.validators import choices_validator


class ProjectModelSerializer(DynamicFieldsModelSerializer):
    """Project model serializer."""

    workers = serializers.SerializerMethodField()
    slots = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()

    activities = ActivityModelSerializer(many=True, read_only=True)

    # choices
    category = serializers.CharField(source="get_category_display")


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
            'finished',
            'workers',
            'slots',
            'activities',
        )
        read_only_fields = (
            'reputation',
            'creator',
            # 'workers',
        )

    def get_workers(self, obj):
        """Return users that works in the project."""

        return WorkerModelSerializer(
            Worker.objects.filter(worker__isnull=False, project=obj),
            many=True,
            fields=('worker', 'position',)
        ).data

    def get_slots(self, obj):
        """Handle slots for workers."""

        return WorkerModelSerializer(
            Worker.objects.filter(worker__isnull=True, project=obj),
            many=True,
            fields=('position',)
        ).data


class ProjectCreateSerializer(serializers.Serializer):
    """Handle project creation."""

    title = serializers.CharField(max_length=50)
    slug_name = serializers.SlugField(
        max_length=8,
        validators=[UniqueValidator(queryset=Project.objects.all())]
    )
    description = serializers.CharField()

    cost = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0
    )

    category = serializers.IntegerField()
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Nested serializers
    slots = WorkerModelSerializer(many=True, required=False)
    activities = ActivityModelSerializer(many=True)

    # Validations
    def validate_category(self, value):
        """Show choices."""
        return choices_validator(value, CATEGORY_CHOICES)

    def create(self, data):
        """Handle project creation."""
        slots = data.pop('slots', None)
        activities = data.pop('activities', None)

        # Project
        project = Project.objects.create(**data, finished=False)

        # slots
        for slot in slots:
            Worker.objects.create(**slot, project=project)

        # activities
        for activity in activities:
            Activity.objects.create(**activity, project=project)

        return project
