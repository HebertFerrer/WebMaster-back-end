"""Donation serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.donations.models import Donation

# Key
from config.settings import STRIPE_SECRET_KEY

# Stripe
import stripe
stripe.api_key = STRIPE_SECRET_KEY


class DonationModelSerializer(serializers.ModelSerializer):
    """Donation model serializer."""

    class Meta:
        """Meta class."""
        model = Donation
        fields = '__all__'


class DonationCreateSerializer(serializers.Serializer):
    """Donation create serializer."""

    stripeToken = serializers.CharField()
    amount = serializers.IntegerField()
    _from = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_amount(self, value):
        """Ammount validator."""
        if value < 1:
            raise serializers.ValidationError('amount must be at least 1$')
        return value

    def create(self, data):
        """Handle creation."""
        amount = data['amount']

        response = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=data['stripeToken'],
            description="Donation"
        )

        database_amount = amount / 100

        print(database_amount, amount)

        if response.paid:
            return Donation.objects.create(
                project=self.context['project'],
                _from=data['_from'],
                amount=database_amount
            )
