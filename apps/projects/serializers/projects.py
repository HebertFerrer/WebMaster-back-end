"""Project serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Project, Worker, Activity
from apps.publications.models import Publication

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

    creator = serializers.StringRelatedField()

    # Nested
    workers = serializers.SerializerMethodField()
    jobs = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    # choices
    category = serializers.CharField(source="get_category_display")


    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'title', 'slug_name',
            'description', 'cost',
            'reputation', 'category',
            'creator', 'finished',
            'workers', 'jobs',
            'publications',
            # 'activities',
        )
        read_only_fields = (
            'reputation',
            'creator',
        )

    def get_workers(self, obj):
        """Return users that works in the project."""

        return WorkerModelSerializer(
            Worker.objects.filter(worker__isnull=False, project=obj),
            many=True,
            fields=('id', 'worker', 'position',),
            context={'action': 'project'}
        ).data

    def get_jobs(self, obj):
        """Handle jobs for workers."""

        return WorkerModelSerializer(
            Worker.objects.filter(worker__isnull=True, project=obj),
            many=True,
            fields=('id', 'position', 'created',)
        ).data

    def get_publications(self, obj):
        """Reurn publications with PublicationModelSerializer."""
        from apps.publications.serializers import PublicationModelSerializer

        return PublicationModelSerializer(
            Publication.objects.filter(project=obj),
            many=True,
            fields=(
                'id',
                'user', 'description',
                'comments', 'likes',
                'pictures',
                'created', 'updated',
            )
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
    jobs = WorkerModelSerializer(many=True, required=False)
    activities = ActivityModelSerializer(many=True)

    # Validations
    def validate_category(self, value):
        """Show choices."""
        return choices_validator(value, CATEGORY_CHOICES)

    def create(self, data):
        """Handle project creation."""
        jobs = data.pop('jobs', None)
        activities = data.pop('activities', None)

        # Project
        project = Project.objects.create(**data, finished=False)

        # jobs
        for job in jobs:
            Worker.objects.create(**job, project=project)

        # activities
        for activity in activities:
            Activity.objects.create(**activity, project=project)

        return project
