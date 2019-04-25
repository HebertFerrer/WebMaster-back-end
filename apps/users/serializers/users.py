"""User serializers."""

# Django
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from apps.users.models import (
    User,
    Profile,
    ProfileWorker,
    ProfileCreator
)

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

        user = User.objects.create(**data, is_active=False)
        profile = Profile.objects.create(
            user=user,
            verified=False,
            born_date=date
        )
        ProfileWorker.objects.create(profile=profile)
        ProfileCreator.objects.create(profile=profile)

        token = Token.objects.create(user=user)
        self.send_confirmation_email(user, token)

        return user

    def send_confirmation_email(self, user, token):
        """Handle sending email to verify account."""

        subject = 'Hola @{}!'.format(user.username)
        from_email = 'noreply@email.com'
        html_content = render_to_string(
            'users/email_verification.html',
            {'token': token, 'user': user, 'host': 'localhost:8000'}
        )
        msg = EmailMultiAlternatives(subject, html_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class VerifyAccountSerializer(serializers.Serializer):
    """Verify user's account and change status 'is_active' to true"""

    token = serializers.CharField()

    def validate_token(self, data):
        """
        Validate the token.
        """

        email_token = data
        time = timezone.now() - timezone.timedelta(days=7) # 7 days ago

        try:
            token = Token.objects.get(key=email_token)
        except Token.DoesNotExist:
            raise serializers.ValidationError('Invalid token.')

        if token.created < time:
            raise serializers.ValidationError('Expired token.')

        self.context['token'] = token

        return data

    def save(self, **kwargs):
        """
        Update user's active status and token.
        """
        old_token = self.context['token']
        user = User.objects.get(auth_token=old_token)

        # Generating new token
        old_token.delete()
        Token.objects.create(user=user)

        # Update user
        user.is_active = True
        user.save()


class UserLoginSerializer(serializers.Serializer):
    """Handle login."""

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """Validate credentials."""

        try:
            user = User.objects.get(
                email=data['email'],
                password=data['password']
            )
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            raise serializers.ValidationError('Account is not active yet.')

        self.context['user'] = user
        return data

    def save(self):
        user = self.context['user']
        return user, user.auth_token.key
