"""Application model."""

# Django
from django.db import models

# Choices
from apps.users.choices import APPLICATION_CHOICES

# Utils
from apps.utils.models import ProjectModel


class Application(ProjectModel):
    """
    Application model handle user request to a specific project position.
    """

    employee = models.ForeignKey('users.User', on_delete=models.CASCADE)
    position = models.ForeignKey('projects.Worker', on_delete=models.CASCADE)

    status = models.CharField(choices=APPLICATION_CHOICES, max_length=30)
