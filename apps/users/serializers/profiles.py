"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    country = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = (
            'picture',
            'biography',
            'born_date',
            'country',
            'verified'
        )
