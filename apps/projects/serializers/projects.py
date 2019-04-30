"""Project serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.projects.models import Project

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer

class ProjectModelSerializer(DynamicFieldsModelSerializer):
    """Project model serializer."""

    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'title',
            'description',
            'reputation'
        )
        read_only_fields = (
            'reputation',
        )
