"""Donation model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Donation(ProjectModel):
    """Donation model."""

    _from = models.ForeignKey('users.User', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
