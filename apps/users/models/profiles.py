"""Profile model."""

# Django
from django.db import models

# Models
from apps.utils.models import ProjectModel

# Choices
from apps.users.choices import (
    GENDER_CHOICES,
    COUNTRY_CHOICES,
    POSITION_CHOICES
)

# Utils
from apps.utils.validators import reputation_validator


class Profile(ProjectModel):
    """Profile model."""

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='statics.users', blank=True, null=True)
    biography = models.TextField(null=True, blank=True)
    born_date = models.DateField()

    # Choices
    gender = models.IntegerField(choices=GENDER_CHOICES)
    country = models.IntegerField(choices=COUNTRY_CHOICES)

    verified = models.BooleanField(
        default=False,
        help_text=(
            'Verificated profiles have better reputation than normal profiles.'
        )
    )


class ProfileCreator(ProjectModel):
    """Creator's profile."""

    reputation = models.SmallIntegerField(default=0, validators=[reputation_validator])
    profile = models.OneToOneField(Profile, related_name='profile_creator', on_delete=models.CASCADE)


class ProfileWorker(ProjectModel):
    """Worker's profile."""

    reputation = models.SmallIntegerField(default=0, validators=[reputation_validator])
    profile = models.OneToOneField(Profile, related_name='profile_worker', on_delete=models.CASCADE)

    # CV
    position = models.IntegerField(choices=POSITION_CHOICES, null=True)
    projects = models.ManyToManyField('projects.Project', through='projects.Worker')
