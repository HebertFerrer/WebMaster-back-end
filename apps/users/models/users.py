"""User model."""

# Models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Utils
from apps.utils.models import ProjectModel

class User(ProjectModel, AbstractUser):
    """Custom user model."""

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be in the format +999999999. From 9 to 15 characters allowed.'
    )
    phone_number = models.CharField(unique=True, max_length=20, validators=[phone_regex])

    REQUIRED_FIELDS = [
        'password',
        'username',
        'first_name',
        'last_name',
    ]
    USERNAME_FIELD = 'email'
