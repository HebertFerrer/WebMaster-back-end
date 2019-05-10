"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from apps.projects.serializers import ProjectModelSerializer

# Models
from apps.users.models import (
    Profile,
    ProfileCreator,
    ProfileWorker
)
from apps.projects.models import Project

# Choices
from apps.users.choices import GENDER_CHOICES

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer


class ProfileCreatorModelSerializer(DynamicFieldsModelSerializer):
    """Profile creator model serializer."""

    # Nested
    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProfileCreator
        fields = (
            'reputation',
            'projects'
        )
        read_only_fields = (
            'reputation',
            'projects'
        )

    def get_projects(self, obj):
        """Add projects via query."""
        return ProjectModelSerializer(
            Project.objects.filter(creator=obj.profile.user),
            many=True,
            read_only=True,
            fields=('title', 'description', 'reputation')
        ).data


class ProfileWorkerModelSerializer(DynamicFieldsModelSerializer):
    """Profile worker model serializer."""

    # Nested
    projects = serializers.SerializerMethodField()

    # Choices
    position = serializers.CharField(source='get_position_display')

    class Meta:
        model = ProfileWorker
        fields = ('reputation', 'projects', 'position',)
        read_only_fields = ('reputation', 'projects',)

    def get_projects(self, obj):
        """Add projects via query."""
        return ProjectModelSerializer(
            Project.objects.filter(workers=obj.profile.user),
            read_only=True,
            many=True,
            fields=('title', 'description', 'reputation')
        ).data


class ProfileModelSerializer(DynamicFieldsModelSerializer):
    """Profile model serializer."""

    # Choices
    gender = serializers.CharField(source='get_gender_display')
    country = serializers.CharField(source='get_country_display')

    # Sub-Profiles (nested)
    profile_worker = serializers.SerializerMethodField()
    profile_creator = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'picture', 'biography',
            'born_date', 'country',
            'gender', 'verified',
            'profile_worker', 'profile_creator',
        )
        read_only_fields = ('verified',)

    def get_profile_worker(self, obj):
        """Dinamically add kwargs to ProfileWorkerModelSerializer."""
        action = self.context.get('action', None)
        context = {'action': action}

        if action == 'list':
            fields = ('reputation',)
            return self.filtered_representation_worker(obj, fields, context)

        if action in ['application', 'project']:
            fields = ('reputation', 'position',)
            return self.filtered_representation_worker(obj, fields, context)

        return ProfileWorkerModelSerializer(obj.profile_worker, read_only=True).data

    def get_profile_creator(self, obj):
        """Dinamically add kwargs to ProfileCreatorModelSerializer."""
        action = self.context.get('action', None)
        context = {'action': action}

        if action == 'list':
            fields = ('reputation',)
            return self.filtered_representation_creator(obj, fields, context)

        if action == 'application':
            fields = ('reputation',)
            return self.filtered_representation_creator(obj, fields, context)

        return ProfileCreatorModelSerializer(obj.profile_creator, read_only=True).data

    def filtered_representation_creator(self, obj, fields, context):
        """Return Model with filtered fields."""
        return ProfileCreatorModelSerializer(
            obj.profile_creator,
            fields=fields,
            context=context
        ).data

    def filtered_representation_worker(self, obj, fields, context):
        """Return Model with filtered fields."""
        return ProfileWorkerModelSerializer(
            obj.profile_worker,
            fields=fields,
            context=context
        ).data
