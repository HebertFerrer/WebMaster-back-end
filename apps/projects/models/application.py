"""Application model."""

# Django
from django.db import models

# Choices
from apps.projects.choices import APPLICATION_CHOICES

# Utils
from apps.utils.models import ProjectModel


class Application(ProjectModel):
    """
    Application model handle user request to a specific project position.
    """

    candidate = models.ForeignKey('users.User', on_delete=models.CASCADE)
    job = models.ForeignKey('projects.Worker', on_delete=models.CASCADE)

    code = models.CharField(max_length=100)
    status = models.IntegerField(choices=APPLICATION_CHOICES)
