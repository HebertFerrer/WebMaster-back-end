"""Calification to worker serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.califications.models import (
    # CalificationToWorker,
    CalificationToProject,
    # CalificationToCreator
)
from apps.projects.models import Project
from apps.users.models import User

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer


# class CalificationToWorkerModelSerializer(DynamicFieldsModelSerializer):
#     """Calification to worker model serializer."""

#     _from = serializers.StringRelatedField()
#     worker = serializers.StringRelatedField()

#     class Meta:
#         """Meta class."""
#         model = CalificationToWorker
#         fields = (
#             'stars', 'comments',
#             '_from', 'worker'
#         )
#         read_only_fields = ('worker',)

#     def validate(self, data):
#         """Handle validation."""
#         request = self.context['request']
#         try:
#             CalificationToWorker.objects.get(
#                 _from=request.user,
#                 worker=self.context['worker']
#             )
#         except CalificationToWorker.DoesNotExist:
#             return data
#         raise serializers.ValidationError('You already qualified this worker.')

#     def create(self, data):
#         """Handle creation."""
#         request = self.context['request']
#         worker = self.context['worker']

#         # Calification
#         instance = CalificationToWorker.objects.create(
#             **data,
#             _from=request.user,
#             worker=self.context['worker']
#         )

#         # Updating reputation
#         queryset = CalificationToWorker.objects.filter(worker=worker).values_list('stars')
#         stars_list = [item[0] for item in queryset]
#         worker.reputation = sum(stars_list) / len(stars_list)
#         worker.save()

#         return instance


class CalificationToProjectModelSerializer(serializers.ModelSerializer):
    """Calification to project model serializer."""

    _from = serializers.StringRelatedField()
    project = serializers.StringRelatedField()

    class Meta:
        """Meta class."""
        model = CalificationToProject
        fields = (
            'stars', 'comment',
            '_from', 'project',
        )
        read_only_fields = ('project',)

    def validate(self, data):
        """Handle validation."""
        request = self.context['request']
        try:
            CalificationToProject.objects.get(
                _from=request.user,
                project=self.context['project']
            )
        except CalificationToProject.DoesNotExist:
            return data
        raise serializers.ValidationError('You already qualified this project.')

    def create(self, data):
        """Handle creation."""
        request = self.context['request']
        project = self.context['project']
        user = User.objects.get(username=project.creator)

        # Calification
        instance = CalificationToProject.objects.create(
            **data,
            _from=request.user,
            project=self.context['project']
        )

        # Updating project reputation
        queryset = CalificationToProject.objects.filter(project=project).values_list('stars')
        stars_list = [item[0] for item in queryset]
        project.reputation = sum(stars_list) / len(stars_list)
        project.save()

        # Updating user reputation
        queryset = Project.objects.filter(creator=user, finished=True).values_list('reputation')
        reputation_list = [item[0] for item in queryset]
        profile_creator = user.profile.profile_creator
        profile_creator.reputation = sum(reputation_list) / len(reputation_list)
        profile_creator.save()
        # import ipdb; ipdb.set_trace()

        return instance


# class CalificationToCreatorModelSerializer(DynamicFieldsModelSerializer):
#     """Calification to creator model serializer."""

#     _from = serializers.StringRelatedField()
#     creator = serializers.StringRelatedField()

#     class Meta:
#         """Meta class."""
#         model = CalificationToCreator
#         fields = (
#             'stars', 'comments',
#             '_from', 'creator'
#         )
#         read_only_fields = ('creator',)

#     def validate(self, data):
#         """Handle validation."""
#         request = self.context['request']
#         try:
#             CalificationToCreator.objects.get(
#                 _from=request.user,
#                 creator=self.context['creator']
#             )
#         except CalificationToCreator.DoesNotExist:
#             return data
#         raise serializers.ValidationError('You already qualified this creator.')

#     def create(self, data):
#         """Handle creation."""
#         request = self.context['request']
#         creator = self.context['creator']

#         # Calification
#         instance = CalificationToCreator.objects.create(
#             **data,
#             _from=request.user,
#             creator=self.context['creator']
#         )

#         # Updating reputation
#         queryset = CalificationToCreator.objects.filter(creator=creator).values_list('stars')
#         stars_list = [item[0] for item in queryset]
#         creator.reputation = sum(stars_list) / len(stars_list)
#         creator.save()

#         return instance
