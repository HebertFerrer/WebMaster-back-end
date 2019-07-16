"""Project serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import (
    Project,
    # Worker,
    # Activity
)
from apps.publications.models import Publication
from apps.donations.models import Donation
from apps.califications.models import CalificationToProject

# Choices
from apps.projects.choices import CATEGORY_CHOICES

# Serializer
# from apps.projects.serializers.worker import WorkerModelSerializer
# from apps.projects.serializers.activity import ActivityModelSerializer

# Validators
from rest_framework.validators import UniqueValidator

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer
from apps.utils.validators import choices_validator


class ProjectModelSerializer(DynamicFieldsModelSerializer):
    """Project model serializer."""

    creator = serializers.StringRelatedField()
    donations = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    # Nested
    # workers = serializers.SerializerMethodField()
    # jobs = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()
    califications = serializers.SerializerMethodField()
    calified = serializers.SerializerMethodField()

    # Filtering report fields
    filter_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    publication_likes = serializers.IntegerField(read_only=True)

    # choices
    category = serializers.CharField(source="get_category_display")

    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'title', 'slug_name',
            'description', 'cost',
            'amount', 'donations',
            'reputation', 'category',
            'calified', 'creator',
            'finished', 'created',
            # 'workers', 'jobs',
            'publications', 'califications',
            # 'activities',
            # Filtered report fields
            'filter_amount', 'publication_likes',
        )
        read_only_fields = (
            'reputation',
            'creator',
            'cost',
            'slug_name',
            # 'finished'
        )

    # def get_workers(self, obj):
    #     """Return users that works in the project."""
    #     view = self.context.get('view', None)
    #     fields = WorkerModelSerializer.Meta.fields

    #     if view is not None:
    #         # Projects
    #         if view.view_name == 'projects' and view.action in view.fields_to_return:
    #             fields = view.fields_to_return[view.action]['workers']

    #     return WorkerModelSerializer(
    #         Worker.objects.filter(worker__isnull=False, project=obj),
    #         many=True,
    #         fields=fields,
    #         context=self.context
    #     ).data

    # def get_jobs(self, obj):
    #     """Handle jobs for workers."""
    #     view = self.context.get('view', None)
    #     fields = WorkerModelSerializer.Meta.fields

    #     if view is not None:
    #         # Projects
    #         if view.view_name == 'projects' and view.action in view.fields_to_return:
    #             fields = view.fields_to_return[view.action]['jobs']

    #     return WorkerModelSerializer(
    #         Worker.objects.filter(worker__isnull=True, project=obj),
    #         many=True,
    #         fields=fields,
    #         context=self.context
    #     ).data

    def get_publications(self, obj):
        """Reurn publications with PublicationModelSerializer."""
        from apps.publications.serializers import PublicationModelSerializer
        view = self.context.get('view', None)
        fields = (
            'id',
            'user', 'project',
            'description',
            'comments', 'likes',
            'picture',
            'created', 'updated',
            'liked',
        )

        if view is not None:
            # Projects
            if view.view_name == 'projects' and view.action in view.fields_to_return:
                fields = view.fields_to_return[view.action]['publications']

        return PublicationModelSerializer(
            Publication.objects.filter(project=obj),
            many=True,
            fields=fields,
            context=self.context
        ).data

    def get_califications(self, obj):
        """Return calification serializer representation."""
        # Serializer
        from apps.califications.serializers import CalificationToProjectModelSerializer

        return CalificationToProjectModelSerializer(
            CalificationToProject.objects.filter(project=obj),
            many=True
        ).data

    def get_amount(self, obj):
        """Return sum of donations."""
        queryset = Donation.objects.filter(project=obj).values_list('amount')
        amounts = [item[0] for item in queryset]
        return sum(amounts)

    def get_donations(self, obj):
        """Return num of donations."""
        return Donation.objects.filter(project=obj).count()

    def get_calified(self, obj):
        """Return if request user already calified the project."""
        request = self.context.get('request', None)

        if request is not None:
            try:
                CalificationToProject.objects.get(
                    _from=self.context['request'].user,
                    project=obj
                )
                return True
            except CalificationToProject.DoesNotExist:
                return False
        return False

    def update(self, instance, data):
        """Handle update to profile."""

        # Updating user instance
        instance.title = data.get('title', instance.title)
        instance.description = data.get('description', instance.description)
        instance.category = int(
            data.get('get_category_display', instance.category))
        instance.finished = int(data.get('finished', instance.finished))
        instance.save()

        return instance


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
    # jobs = WorkerModelSerializer(many=True, required=False)

    # Validations
    def validate_category(self, value):
        """Show choices."""
        return choices_validator(value, CATEGORY_CHOICES)

    def create(self, data):
        """Handle project creation."""
        # jobs = data.pop('jobs', None)

        # Project
        project = Project.objects.create(**data, finished=False)

        # jobs
        # if jobs is not None:
        #     for job in jobs:
        #         Worker.objects.create(**job, project=project)

        return project
