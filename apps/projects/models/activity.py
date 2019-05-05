"""Activity model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel

class Activity(ProjectModel):
    """Activity model."""

    description = models.CharField(max_length=200)
    duration = models.IntegerField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
