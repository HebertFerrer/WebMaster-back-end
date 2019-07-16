"""Follow serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from apps.users.serializers import UserModelSerializer

# Models
from apps.users.models import Follow, User

# Utils
import uuid
from apps.utils.serializers import DynamicFieldsModelSerializer

class FollowModelSerializer(DynamicFieldsModelSerializer):
    """Follow model serializer."""

    follower = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()

    status = serializers.CharField(source='get_status_display')

    class Meta:
        """Meta class."""
        model = Follow
        fields = (
            'follower', 'followed',
            'status', 'code',
            'created',
        )

    def get_follower(self, obj):
        """Return followers information."""
        view = self.context.get('view', None)
        fields = (
            'email', 'username',
            'phone_number', 'first_name',
            'last_name', 'profile',
        )

        if view is not None:
            # Users
            if view.view_name == 'users' and view.action in view.fields_to_return:
                fields = view.fields_to_return[view.action]['followers']['follower']

        return UserModelSerializer(obj.follower, fields=fields, context=self.context).data

    def get_followed(self, obj):
        """Return followers information."""
        view = self.context.get('view', None)
        fields = (
            'email', 'username',
            'phone_number', 'first_name',
            'last_name', 'profile',
        )

        if view is not None:
            # Users
            if view.view_name == 'users' and view.action in view.fields_to_return:
                fields = view.fields_to_return[view.action]['followeds']['followed']

        return UserModelSerializer(obj.followed, fields=fields, context=self.context).data



class FollowCreateSerializer(serializers.Serializer):
    """Handle follow request creation."""

    follower = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        """
        Validate if there is already a follow request
        in status 'Waiting'.
        """
        request = self.context['request']
        try:
            Follow.objects.get(
                follower=request.user,
                followed=self.context['user'],
                status=3
            )
        except Follow.DoesNotExist:
            return data
        raise serializers.ValidationError('You already send a follow request to this user')

    def create(self, data):
        """Handle creation."""
        followed = self.context['user']
        code = uuid.uuid4()

        while True:
            try:
                Follow.objects.get(code=code)
            except Follow.DoesNotExist:
                break
            code = uuid.uuid4()

        return Follow.objects.create(
            follower=data['follower'],
            followed=followed,
            status=3,
            code=code
        )


class FollowAcceptSerializer(serializers.Serializer):
    """Handle accepting follow request."""

    def update(self, instance, validated_data):
        """Handle status update."""
        if instance.status == 1:
            raise serializers.ValidationError(
                "Follow request already accepted, not in 'Waiting' status."
            )
        elif instance.status == 2:
            raise serializers.ValidationError(
                "Follow request already rejected, not in 'Waiting' status."
            )
        else:
            instance.status = 1
            instance.save()
            return instance


class FollowRejectSerializer(serializers.Serializer):
    """Reject follow request."""

    def update(self, instance, validated_data):
        """Handle status update."""
        if instance.status == 1:
            raise serializers.ValidationError(
                "Follow request already accepted, not in 'Waiting' status."
            )
        elif instance.status == 2:
            raise serializers.ValidationError(
                "Follow request already rejected, not in 'Waiting' status."
            )
        else:
            instance.status = 2
            instance.save()
            return instance
