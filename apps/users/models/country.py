"""Country model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel


class Country(ProjectModel):
    """Country model."""

    name = models.CharField(max_length=60)
