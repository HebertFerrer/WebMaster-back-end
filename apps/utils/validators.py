"""Validators."""

# Django
from django.core.exceptions import ValidationError


def reputation_validator(value):
    """Validates that reputation is between 0 and 5."""

    if value < 0 or value > 5:
        raise ValidationError(
            'Reputation must be a integer between 0 and 5.'
        )
