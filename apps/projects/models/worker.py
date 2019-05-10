"""Worker model."""

# Django
from django.db import models

# Choices
from apps.users.choices import POSITION_CHOICES

# Utils
from apps.utils.models import ProjectModel


class Worker(ProjectModel):
    """Project worker."""

    worker = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True)

    position = models.IntegerField(choices=POSITION_CHOICES)


    def __str__(self):
        return self.position
