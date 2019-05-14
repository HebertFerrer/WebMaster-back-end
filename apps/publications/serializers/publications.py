"""Publication serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from apps.publications.serializers.pictures import (
    PictureModelSerializer
)

# Models
from apps.publications.models import Publication, Like, Picture, Comment
from apps.users.models import User

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer


class PublicationModelSerializer(DynamicFieldsModelSerializer):
    """Publication model seializer."""

    project = serializers.StringRelatedField()
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()

    # Nested
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = (
            'id',
            'user', 'project',
            'description',
            'comments', 'likes',
            'pictures',
            'created', 'updated',
        )

    def get_user(self, obj):
        """Show user that makes the publication."""
        user = User.objects.get(username=obj.project.creator)
        return user.username

    def get_likes(self, obj):
        """Show user that makes the publication."""
        try:
            likes_count = Like.objects.filter(publication=obj).count()
        except Like.DoesNotExist:
            likes_count = 0
        return likes_count

    def get_comments(self, obj):
        """Get CommentModelSerializer representation."""
        from apps.publications.serializers import CommentModelSerializer

        return CommentModelSerializer(
            Comment.objects.filter(publication=obj),
            many=True
        ).data

    def get_pictures(self, obj):
        """Retrieve pictures."""
        return PictureModelSerializer(
            Picture.objects.filter(publication=obj),
            many=True
        ).data


class PublicationCreateSerializer(serializers.Serializer):
    """Publication create serializer."""

    description = serializers.CharField()
    pictures = PictureModelSerializer(many=True, required=False)

    def create(self, data):
        """Handle publication create."""
        pictures_data = data.pop('pictures', None)

        publication = Publication.objects.create(**data, project=self.context['project'])
        for picture_data in pictures_data:
            Picture.objects.create(**picture_data, publication=publication)

        return publication
