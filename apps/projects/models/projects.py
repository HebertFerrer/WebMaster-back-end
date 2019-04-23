"""Projects model."""

# Django
from django.db import models

# Models
from apps.utils.models import ProjectModel

# Utils
from apps.utils.validators import reputation_validator


class Project(ProjectModel):
    """Project model."""

    title = models.CharField(max_length=50)
    description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    reputation = models.SmallIntegerField(default=0, validators=[reputation_validator])
    category = models.ForeignKey('projects.Category', on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey('users.ProfileCreator', on_delete=models.SET_NULL, null=True)
    finished = models.BooleanField(default=False)
