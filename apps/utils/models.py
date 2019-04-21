"""Utils models."""

# Django
from django.db import models


class ProjectModel(models.Model):
    """General model.

    By default add the following fields:
    - Created
    - Updated
    """

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""
        ordering = ('-created')
