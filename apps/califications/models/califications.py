"""Calification model."""

# Django
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Utils
from apps.utils.models import ProjectModel
from apps.utils.validators import reputation_validator


class Calification(ProjectModel):
    """Calification model."""

    stars = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[reputation_validator]
    )
    comment = models.TextField()

    _from = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        """Meta class."""
        abstract = True


# class CalificationToWorker(Calification):
#     """Calification to worker."""

#     worker = models.ForeignKey('users.ProfileWorker', on_delete=models.CASCADE)


class CalificationToProject(Calification):
    """Calification to project."""

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)


# class CalificationToCreator(Calification):
#     """Calification to Creator."""

#     creator = models.ForeignKey('users.ProfileCreator', on_delete=models.CASCADE)
