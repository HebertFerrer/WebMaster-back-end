"""Follow model."""

# Django
from django.db import models

# Utils
from apps.utils.models import ProjectModel
from apps.users.choices import FOLLOW_CHOICES

class Follow(ProjectModel):
    """Follow model."""

    follower = models.ForeignKey('users.User', related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey('users.User', related_name='followed', on_delete=models.CASCADE)

    code = models.CharField(max_length=100)
    status = models.IntegerField(choices=FOLLOW_CHOICES)
