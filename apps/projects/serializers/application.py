"""Application serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Application, Worker

# Serializers
from apps.projects.serializers import WorkerModelSerializer

# Choices
from apps.projects.choices import APPLICATION_CHOICES

# Utils
from apps.utils.validators import choices_validator
import uuid


class ApplicationModelSerializer(serializers.ModelSerializer):
    """Application model serializer."""

    # Nested
    candidate = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()

    # Choices
    status = serializers.CharField(source='get_status_display')

    class Meta:
        """Meta class."""
        model = Application
        fields = (
            'candidate', 'job',
            'code', 'status',
        )
        read_only_fields = (
            'status', 'candidate',
            'code',
        )

    def validate_status(self, value):
        """Show choices."""
        return choices_validator(value, APPLICATION_CHOICES)

    def get_candidate(self, obj):
        """Return usermodelserializer representation."""

        # Serializers
        from apps.users.serializers import UserModelSerializer

        return UserModelSerializer(
            obj.candidate,
            fields=('username', 'profile',),
            context={'action': 'application'}
        ).data

    def get_job(self, obj):
        """Return WokerModelSerializer representation."""
        action = self.context.get('action', None)

        if action == 'list':
            return WorkerModelSerializer(
                obj.job,
                fields=('id', 'position',)
            ).data

        return WorkerModelSerializer(
            obj.job,
            fields=('project', 'position',)
        ).data


class ApplicationCreateSerializer(serializers.Serializer):
    """Application create serializer."""

    candidate = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        """Validate that position is available."""
        try:
            job = Worker.objects.get(
                worker__isnull=True,
                pk=self.context['job_pk']
            )
        except Worker.DoesNotExist:
            raise serializers.ValidationError(
                'The job you are trying to applicate for is already taken or does not exists.'
            )
        self.context['job'] = job

        try:
            Application.objects.get(
                candidate=data['candidate'],
                job=job
            )
        except Application.DoesNotExist:
            return data
        raise serializers.ValidationError('You already send an application request for this job')

    def create(self, data):
        """Handle creation."""
        candidate = data['candidate']
        job = self.context['job']
        code = uuid.uuid4()

        while True:
            try:
                Application.objects.get(code=code)
            except Application.DoesNotExist:
                break
            code = uuid.uuid4()

        return Application.objects.create(
            candidate=candidate,
            job=job,
            code=code,
            status=3
        )


class ApplicationRejectSerializer(serializers.Serializer):
    """Reject application request serializer."""


    def update(self, instance, data):
        """Update status."""
        status = int(instance.status)
        if status == 1:
            raise serializers.ValidationError(
                "Application request already accepted, not in 'Waiting' status."
            )
        elif status == 2:
            raise serializers.ValidationError(
                "Application request already rejected, not in 'Waiting' status."
            )
        else:
            instance.status = 2
            instance.save()
            return instance


class ApplicationAcceptSerializer(serializers.Serializer):
    """Accept application request serializer."""

    def update(self, instance, data):
        """Update status."""
        if instance.status == 1:
            raise serializers.ValidationError(
                "Application request already accepted, not in 'Waiting' status."
            )
        elif instance.status == 2:
            raise serializers.ValidationError(
                "Application request already rejected, not in 'Waiting' status."
            )
        else:
            instance.status = 1
            instance.save()

            # Worker
            worker = instance.job
            worker.worker = instance.candidate
            worker.save()

            return instance
