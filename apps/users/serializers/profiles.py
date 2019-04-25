"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.users.models import (
    Profile,
    ProfileCreator,
    ProfileWorker
)


class ProfileCreatorModelSerializer(serializers.ModelSerializer):
    """Profile creator model serializer."""

    class Meta:
        model = ProfileCreator
        fields = (
            'reputation',
        )
        # read_only = (
        #     'reputation',
        #     'projects'
        # )


class ProfileWorkerModelSerializer(serializers.ModelSerializer):
    """Profile worker model serializer."""

    projects = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProfileWorker
        fields = (
            'reputation',
            'projects',
        )
        # read_only = (
        #     'reputation',
        #     'projects'
        # )


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    country = serializers.StringRelatedField()

    # Sub-Profiles
    profile_worker = ProfileWorkerModelSerializer(read_only=True)
    profile_creator = ProfileCreatorModelSerializer(read_only=True)

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
        # read_only = ('verified',)
