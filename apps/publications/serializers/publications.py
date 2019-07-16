"""Publication serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
# from apps.publications.serializers.pictures import (
#     PictureModelSerializer
# )

# Models
from apps.publications.models import (
    Publication,
    # LikeToComment,
    LikeToPublication,
    # Picture,
    Comment
)
from apps.users.models import User

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer


class PublicationModelSerializer(DynamicFieldsModelSerializer):
    """Publication model seializer."""

    project = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    # pictures = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    # Nested
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = (
            'id',
            'user', 'project',
            'description',
            'comments', 'likes',
            'picture',
            'created', 'updated',
            'liked',
        )

    def get_user(self, obj):
        """Show user that makes the publication."""
        # Serializer
        from apps.users.serializers import UserModelSerializer
        try:
            user = User.objects.get(username=obj.project.creator)
        except User.DoesNotExist:
            return None
        return UserModelSerializer(user, fields=('username', 'profile',)).data

    def get_likes(self, obj):
        """Show user that makes the publication."""
        try:
            likes_count = LikeToPublication.objects.filter(
                publication=obj).count()
        except LikeToPublication.DoesNotExist:
            likes_count = 0
        return likes_count

    def get_comments(self, obj):
        """Get CommentModelSerializer representation."""
        from apps.publications.serializers import CommentModelSerializer

        return CommentModelSerializer(
            Comment.objects.filter(publication=obj),
            many=True
        ).data

    def get_project(self, obj):
        """Return project in serializer representation."""
        # Serializer
        from apps.projects.serializers import ProjectModelSerializer

        return ProjectModelSerializer(obj.project, fields=('title', 'slug_name', 'finished',)).data

    # def get_pictures(self, obj):
    #     """Retrieve pictures."""
    #     # view = self.context.get('view', None)
    #     # fields = PictureModelSerializer.Meta.fields

    #     # if view is not None:
    #     #     # Projects
    #     #     if view.view_name == 'projects' and view.action in view.fields_to_return:
    #     #         fields = view.fields_to_return[view.action]['publications']['pictures']

    #     return PictureModelSerializer(
    #         Picture.objects.filter(publication=obj),
    #         many=True,
    #         # fields=fields,
    #         context=self.context
    #     ).data

    def get_liked(self, obj):
        """Return if request user already liked this publication."""
        for item in LikeToPublication.objects.filter(publication=obj):
            if self.context['request'].user == item.user:
                return True
        return False


class PublicationCreateSerializer(serializers.Serializer):
    """Publication create serializer."""

    description = serializers.CharField()
    picture = serializers.ImageField(required=False)

    def create(self, data):
        """Handle publication create."""
        # pictures_data = data.pop('pictures', None)

        publication = Publication.objects.create(
            **data, project=self.context['project'])
        # if pictures_data is not None:
        #     for picture_data in pictures_data:
        #         Picture.objects.create(**picture_data, publication=publication)

        return publication
