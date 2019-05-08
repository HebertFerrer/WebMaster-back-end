"""Activity model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel

class Activity(ProjectModel):
    """Activity model."""

    description = models.CharField(max_length=200)
    duration = models.IntegerField()
    finished = models.BooleanField(default=False)
    project = models.ForeignKey(
        'projects.Project',
        related_name='activities',
        on_delete=models.CASCADE
    )
