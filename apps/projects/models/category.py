"""Category model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Category(ProjectModel):
    """Category model."""

    name = models.CharField(max_length=120)
