"""Filter custom classes."""

# Filter
from django_filters import rest_framework as filters

# Models
from apps.users.models import User

class UserFilter(filters.FilterSet):
    """User filter class."""

    min_reputation = filters.NumericRangeFilter()

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'username',
            'profile__verified',
            'profile__born_date',
            # 'profile__profile_worker__reputation',
        )
