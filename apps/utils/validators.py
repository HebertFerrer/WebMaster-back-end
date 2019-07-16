"""Validators."""

# Django
from django.core.exceptions import ValidationError

# Serializers
from rest_framework import serializers

def reputation_validator(value):
    """Validates that reputation is between 0 and 5."""

    if value < 0 or value > 5:
        raise ValidationError(
            'Reputation must be a integer between 0 and 5.'
        )

def choices_validator(value, CHOICES_TUPLE):
    """Return choices info."""

    choices = [c[0] for c in CHOICES_TUPLE]

    value = int(value)
    if value not in choices:
        fields = ''
        for choice in CHOICES_TUPLE:
            fields += '| {} - {} |'.format(choice[0], choice[1])
        raise serializers.ValidationError('Option is not valid, try: {}'.format(fields))
    return value
