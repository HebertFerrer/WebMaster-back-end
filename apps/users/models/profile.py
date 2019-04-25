"""Profile model."""

# Django
from django.db import models

# Models
from apps.utils.models import ProjectModel

# Utils
from apps.utils.validators import reputation_validator


class Profile(ProjectModel):
    """Profile model."""
    # ARGENTINA = 0
    # BRASIL = 1
    # BOLIVIA = 2
    # CHILE = 3
    # COLOMBIA = 4
    # ECUADOR = 5
    # PARAGUAY = 6
    # PUERTO_RICO = 7
    # PERU = 8
    # URUGUAY = 9
    # VENEZUELA = 10

    # COUNTRY_CHOICES = (
    #     (ARGENTINA, 'Argentina'),
    #     (BRASIL, 'Brasil'),
    #     (BOLIVIA, 'Bolivia'),
    #     (CHILE, 'Chile'),
    #     (COLOMBIA, 'Colombia'),
    #     (PARAGUAY, 'Ecuador'),
    #     (PUERTO_RICO, 'Puerto rico'),
    #     (PERU, 'Peru'),
    #     (URUGUAY, 'Uruguay'),
    #     (VENEZUELA, 'Venezuela'),
    # )

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='statics.users', blank=True, null=True)
    biography = models.TextField(null=True, blank=True)
    born_date = models.DateField()
    country = models.ForeignKey('users.Country', on_delete=models.SET_NULL, null=True)
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
    projects = models.ManyToManyField(
        'projects.Project',
        through='projects.Worker'
    )
