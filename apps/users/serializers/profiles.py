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

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer

class ProfileCreatorModelSerializer(DynamicFieldsModelSerializer):
    """Profile creator model serializer."""

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
            Project.objects.filter(creator=obj),
            many=True,
            fields=('title', 'description', 'reputation')
        ).data


class ProfileWorkerModelSerializer(DynamicFieldsModelSerializer):
    """Profile worker model serializer."""

    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProfileWorker
        fields = (
            'reputation',
            'projects',
        )
        read_only_fields = (
            'reputation',
            'projects'
        )

    def get_projects(self, obj):
        """Add projects via query."""
        return ProjectModelSerializer(
            obj.projects,
            many=True,
            fields=('title', 'description', 'reputation')
        ).data


class ProfileModelSerializer(DynamicFieldsModelSerializer):
    """Profile model serializer."""

    country = serializers.StringRelatedField()

    # Sub-Profiles
    profile_worker = serializers.SerializerMethodField()
    profile_creator = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'picture',
            'biography',
            'born_date',
            'country',
            'verified',
            'profile_worker',
            'profile_creator',
        )
        read_only_fields = ('verified',)

    def get_profile_worker(self, obj):
        """Dinamically add kwargs to ProfileWorkerModelSerializer."""
        if self.context['action'] == 'list':
            fields = (
                'reputation',
            )
            return ProfileWorkerModelSerializer(
                obj.profile_worker,
                read_only=True,
                fields=fields
            ).data
        return ProfileWorkerModelSerializer(obj.profile_worker, read_only=True).data

    def get_profile_creator(self, obj):
        """Dinamically add kwargs to ProfileCreatorModelSerializer."""
        if self.context['action'] == 'list':
            fields = (
                'reputation',
                'projects',
            )
            return ProfileCreatorModelSerializer(
                obj.profile_creator,
                read_only=True,
                fields=fields
            ).data
        return ProfileCreatorModelSerializer(obj.profile_creator, read_only=True).data
