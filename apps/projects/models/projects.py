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
    slug_name = models.SlugField()
    description = models.TextField()

    cost = models.DecimalField(max_digits=12, decimal_places=2)
    reputation = models.SmallIntegerField(default=0, validators=[reputation_validator])

    category = models.IntegerField(choices=CATEGORY_CHOICES)
    creator = models.ForeignKey('users.ProfileCreator', on_delete=models.SET_NULL, null=True)

    finished = models.BooleanField(default=False)

    def __str__(self):
        """Return project title."""
        return self.title
