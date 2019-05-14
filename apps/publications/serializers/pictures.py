"""Picture serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.publications.models import Picture


class PictureModelSerializer(serializers.ModelSerializer):
    """Picture model serializer."""

    class Meta:
        model = Picture
        fields = ('id', 'picture', 'publication',)
        read_only_fields = ('publication',)

    def create(self, data):
        """Handle picture creation."""
        return Picture.objects.create(**data, publication=self.context['publication'])
