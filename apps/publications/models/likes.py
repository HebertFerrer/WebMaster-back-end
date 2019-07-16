"""Likes model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class LikeAbstract(ProjectModel):
    """Abstract like model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        """Meta class."""
        abstract = True


class LikeToPublication(LikeAbstract):
    """Like to Publication model."""

    publication = models.ForeignKey('publications.Publication', on_delete=models.CASCADE)

# Si da el tiro se implementa

# class LikeToComment(LikeAbstract):
#     """Like to Comment model."""

#     comment = models.ForeignKey('publications.Comment', on_delete=models.CASCADE)
