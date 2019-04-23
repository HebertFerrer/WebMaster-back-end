"""Worker model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Worker(ProjectModel):
    """Project worker."""

    worker = models.ForeignKey('users.ProfileWorker', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True)

    position = models.CharField(max_length=100)
