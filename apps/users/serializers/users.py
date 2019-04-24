"""User serializers."""

# Django
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from apps.users.models import User, Profile

# Serializers
from apps.users.serializers import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'email',
            'username',
            'phone_number',
            'first_name',
            'last_name',
            'profile',
        )


class UserSignupSerializer(serializers.Serializer):
    """Handles Signup action."""

    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        max_length=30,
        min_length=2,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Passwords
    password = serializers.CharField()
    password_confirmation = serializers.CharField()

    # Phone number
    phone_regex = RegexValidator(
        regex=r'^\+1?\d{9,15}$',
        message='Phone number must be in the format +999999999. From 9 to 15 characters allowed.'
    )
    phone_number = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(User.objects.all()),
            phone_regex
        ]
    )

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    born_date = serializers.DateField()

    def validate(self, data):
        """Validate password and password_confirmation are the same."""

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, data):
        """Handle profile creation."""
        data.pop('password_confirmation')
        date = data.pop('born_date')

        user = User.objects.create(**data, is_active=True)
        Profile.objects.create(
            user=user,
            verified=False,
            born_date=date
        )
        return user
