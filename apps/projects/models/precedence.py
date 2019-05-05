"""Precedence model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Precedence(ProjectModel):
    """Precedence model."""

    activity = models.ForeignKey('projects.Activity', on_delete=models.CASCADE)
    precedence = models.ForeignKey(
        'projects.Activity',
        related_name='precedence_activity',
        on_delete=models.CASCADE
    )
