"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from apps.projects.serializers import ProjectModelSerializer

# Models
from apps.users.models import (
    Profile,
    ProfileCreator,
    # ProfileWorker
)
from apps.projects.models import Project

# Choices
from apps.users.choices import GENDER_CHOICES

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer
from apps.utils.validators import choices_validator


class ProfileCreatorModelSerializer(DynamicFieldsModelSerializer):
    """Profile creator model serializer."""

    # Nested
    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProfileCreator
        fields = ('reputation', 'projects')
        read_only_fields = ('reputation', 'projects')

    def get_projects(self, obj):
        """Add projects via query."""
        view = self.context.get('view', None)
        fields = (
            'title', 'slug_name',
            'finished', 'created',
        )

        # if view is not None:

        #     # Users
        #     if view.view_name == 'users' and view.action in view.fields_to_return:
        #         fields = view.fields_to_return[view.action]['profile']['profile_creator']['projects']


        return ProjectModelSerializer(
            Project.objects.filter(creator=obj.profile.user),
            many=True,
            fields=fields,
            context=self.context
        ).data


# class ProfileWorkerModelSerializer(DynamicFieldsModelSerializer):
#     """Profile worker model serializer."""

#     # Nested
#     projects = serializers.SerializerMethodField()

#     # Choices
#     position = serializers.CharField(source='get_position_display')

#     class Meta:
#         model = ProfileWorker
#         fields = ('reputation', 'projects', 'position',)
#         read_only_fields = ('reputation', 'projects',)

#     def get_projects(self, obj):
        # """Add projects via query."""
        # view = self.context.get('view', None)
        # fields = (
        #     'title', 'slug_name',
        #     'description', 'cost',
        #     'reputation', 'category',
        #     'creator', 'finished',
        # )

        # if view is not None:

        #     # Users
        #     if view.view_name == 'users' and view.action in view.fields_to_return:
        #         fields = view.fields_to_return[view.action]['profile']['profile_worker']['projects']

        # return ProjectModelSerializer(
        #     Project.objects.filter(workers=obj.profile.user),
        #     many=True,
        #     fields=fields,
        #     context=self.context
        # ).data


class ProfileModelSerializer(DynamicFieldsModelSerializer):
    """Profile model serializer."""

    # Choices
    gender = serializers.CharField(source="get_gender_display")

    # Sub-Profiles (nested)
    # profile_worker = serializers.SerializerMethodField()
    profile_creator = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'picture', 'biography',
            'born_date', 'gender',
            'verified',
            # 'profile_worker',
            'profile_creator',
        )
        read_only_fields = ('verified',)

    # def get_profile_worker(self, obj):
    #     """Dinamically add kwargs to ProfileWorkerModelSerializer."""
    #     view = self.context.get('view', None)
    #     fields = ('reputation', 'projects', 'position',)

    #     if view is not None:
    #         # Users
    #         if view.view_name == 'users' and view.action in view.fields_to_return:
    #             fields = view.fields_to_return[view.action]['profile']['profile_worker']

    #         # Projects
    #         if view.view_name == 'projects' and view.action in view.fields_to_return:
    #             fields = view.fields_to_return[view.action][
    #                 'workers']['worker']['profile']['profile_worker']

    #     # if action in ['application':
    #     #     fields = ('reputation', 'position',)

    #     return ProfileWorkerModelSerializer(
    #         obj.profile_worker,
    #         fields=fields,
    #         context=self.context
    #     ).data

    def get_profile_creator(self, obj):
        """Dinamically add kwargs to ProfileCreatorModelSerializer."""
        view = self.context.get('view', None)
        fields = ('reputation', 'projects',)

        if view is not None:
            # Users
            if view.view_name == 'users' and view.action in view.fields_to_return:
                fields = view.fields_to_return[view.action]['profile']['profile_creator']

        # if action == 'application':
        #     fields = ('reputation',)

        return ProfileCreatorModelSerializer(
            obj.profile_creator,
            fields=fields,
            context=self.context
        ).data

    def validate_gender(self, value):
        """Show choices."""
        return choices_validator(value, GENDER_CHOICES)
