"""Like serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.publications.models import Like

# Utils
from apps.utils.serializers import DynamicFieldsModelSerializer

class LikeModelSerializer(DynamicFieldsModelSerializer):
    """Like model serializer."""

    # Nested
    user = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'user', 'publication')
        read_only_fields = ('publication',)

    def get_user(self, obj):
        """Return UserModelSerializer representation."""
        from apps.users.serializers import UserModelSerializer

        return UserModelSerializer(
            obj.user,
            fields=('username','profile',),
            context={'action': 'like'}
        ).data


    def validate(self, data):
        """Handle validations."""
        user = self.context['request'].user
        publication = self.context['publication']
        queryset = Like.objects.filter(publication=publication).values_list('user')
        pk_list = [item[0] for item in queryset]

        if user.pk in pk_list:
            raise serializers.ValidationError(
                'You already liked this publication'
            )

        return data

    def create(self, data):
        """Handle like create."""
        request = self.context['request']
        return Like.objects.create(
            user=request.user,
            publication=self.context['publication']
        )
