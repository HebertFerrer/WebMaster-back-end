"""Calification model."""

# Django
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Utils
from apps.utils.models import ProjectModel


class Calification(ProjectModel):
    """Calification model."""

    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comments = models.TextField()

    _from = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        """Meta class."""
        abstract = True


class CalificationToWorker(Calification):
    """Calification to worker."""

    worker = models.ForeignKey('users.ProfileWorker', on_delete=models.CASCADE)


class CalificationToProject(Calification):
    """Calification to project."""

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)


class CalificationToCreator(Calification):
    """Calification to Creator."""

    creator = models.ForeignKey('users.ProfileCreator', on_delete=models.CASCADE)
