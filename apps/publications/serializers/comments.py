"""Comment serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.publications.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'comment', 'user',
            'created', 'updated',
        )

    def create(self, data):
        """Handle comment create."""
        request = self.context['request']
        publication = self.context['publication']

        return Comment.objects.create(
            **data,
            publication=publication,
            user=request.user
        )
