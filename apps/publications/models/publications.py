"""Publication models."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Publication(ProjectModel):
    """Publication model."""

    description = models.TextField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to='publications',
        blank=True,
        null=True
    )

    # m2m
    # comments = models.ManyToManyField(
    #     'users.User',
    #     related_name='comments',
    #     through='publications.Comment'
    # )
    # likes = models.ManyToManyField(
    #     'users.User',
    #     related_name='likes',
    #     through='publications.Like'
    # )
