"""Comments model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Comment(ProjectModel):
    """Comment model."""

    comment = models.TextField()

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    publication = models.ForeignKey('publications.Publication', on_delete=models.CASCADE)
