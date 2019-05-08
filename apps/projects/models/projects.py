"""Projects model."""

# Django
from django.db import models

# Models
from apps.utils.models import ProjectModel

# Choices
from apps.projects.choices import CATEGORY_CHOICES

# Utils
from apps.utils.validators import reputation_validator


class Project(ProjectModel):
    """Project model."""

    title = models.CharField(max_length=50)
    slug_name = models.SlugField(unique=True)
    description = models.TextField()

    cost = models.DecimalField(max_digits=12, decimal_places=2)
    reputation = models.SmallIntegerField(default=0, validators=[reputation_validator])

    category = models.IntegerField(choices=CATEGORY_CHOICES)
    creator = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    # m2m
    workers = models.ManyToManyField(
        'users.User',
        related_name='workers',
        through='projects.Worker'
    )

    finished = models.BooleanField(default=False)

    def __str__(self):
        """Return project title."""
        return self.title
