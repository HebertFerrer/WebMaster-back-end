"""User serializers."""

# Django
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from apps.users.models import (
    User,
    Profile,
    # ProfileWorker,
    ProfileCreator,
    Follow
)

# Choices
from apps.users.choices import GENDER_CHOICES, COUNTRY_CHOICES

# Serializers
from apps.users.serializers import ProfileModelSerializer

# Utils
from apps.utils.validators import choices_validator
from apps.utils.serializers import DynamicFieldsModelSerializer


class UserModelSerializer(DynamicFieldsModelSerializer):
    """User model serializer."""

    # Now profile is writable
    profile = ProfileModelSerializer()

    followers = serializers.SerializerMethodField()
    followeds = serializers.SerializerMethodField()
    follow_requests = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'email', 'username',
            'phone_number', 'first_name',
            'last_name', 'profile',
            'followers', 'followeds',
            'follow_requests',
        )

    # def get_profile(self, obj):
        # """Dinamically add kwargs to ProfileModelSerializer."""
        # view = self.context.get('view', None)
        # fields = (
        #     'picture', 'biography',
        #     'born_date', 'country',
        #     'gender', 'verified',
        #     'profile_worker', 'profile_creator',
        # )

        # if view is not None:
        #     # Users
        #     if view.view_name == 'users' and view.action in view.fields_to_return:
        #         fields = view.fields_to_return[view.action]['profile']

        #     # Projects
        #     elif view.view_name == 'projects' and view.action in view.fields_to_return:
        #         fields = view.fields_to_return[view.action]['workers']['worker']['profile']


        # # if action in ['application', 'project']:
        # #     fields = (
        # #         'picture',
        # #         'profile_worker',
        # #     )

        # # if action == 'like':
        # #     fields = (
        # #         'picture',
        # #     )

        # return ProfileModelSerializer(obj.profile, fields=fields, context=self.context).data

    def get_followers(self, obj):
        """Return followers information."""
        # Serializer
        from apps.users.serializers import FollowModelSerializer

        view = self.context.get('view', None)
        fields = (
            'email', 'username',
            'phone_number', 'first_name',
            'last_name',
        )

        if view is not None:
            # Users
            if view.view_name == 'users' and view.action in view.fields_to_return:
                fields = view.fields_to_return[view.action]['followers']

        return FollowModelSerializer(
            Follow.objects.filter(followed=obj, status=1),
            fields=fields,
            context=self.context,
            many=True
        ).data

    def get_followeds(self, obj):
        """Return followers information."""
        # Serializer
        from apps.users.serializers import FollowModelSerializer

        view = self.context.get('view', None)
        fields = (
            'email', 'username',
            'phone_number', 'first_name',
            'last_name',
        )

        if view is not None:
            # Users
            if view.view_name == 'users' and view.action in view.fields_to_return:
                fields = view.fields_to_return[view.action]['followeds']

        return FollowModelSerializer(
            Follow.objects.filter(follower=obj, status=1),
            fields=fields,
            context=self.context,
            many=True
        ).data

    def get_follow_requests(self, obj):
        """Return follow requests."""
        # Serializer
        from apps.users.serializers import FollowModelSerializer
        fields = (
            'follower', 'status',
            'code', 'created',
        )

        return FollowModelSerializer(
            Follow.objects.filter(followed=obj, status=3),
            fields=fields,
            context=self.context,
            many=True
        ).data

    def update(self, instance, data):
        """Handle update with nested profile data."""
        profile_data = data.pop('profile', None)
        profile = instance.profile

        # Updating user instance
        instance.username = data.get('username', instance.username)
        instance.email = data.get('email', instance.email)
        instance.phone_number = data.get('phone_number', instance.phone_number)
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        instance.save()

        # Updating profile nested instance
        if profile_data is not None:
            profile.picture = profile_data.get('picture', profile.picture)
            profile.biography = profile_data.get('biography', profile.biography)
            profile.born_date = profile_data.get('born_date', profile.born_date)
            profile.gender = int(profile_data.get('get_gender_display', profile.gender))
            profile.save()

        return instance



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
        regex=r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$',
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

    # Choices
    gender = serializers.IntegerField()
    # country = serializers.IntegerField()


    def validate(self, data):
        """Validate password and password_confirmation are the same."""

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords must match.')

        return data

    def validate_gender(self, value):
        """Show choices."""
        return choices_validator(value, GENDER_CHOICES)

    def validate_country(self, value):
        """Show choices."""
        return choices_validator(value, COUNTRY_CHOICES)

    def create(self, data):
        """Handle profile creation."""
        data.pop('password_confirmation')
        date = data.pop('born_date')
        gender = data.pop('gender')

        user = User.objects.create(**data, is_active=True)
        profile = Profile.objects.create(
            user=user,
            verified=False,
            born_date=date,
            gender=gender
        )
        # ProfileWorker.objects.create(profile=profile)
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
            {'token': token, 'user': user, 'host': 'localhost:8080'}
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
