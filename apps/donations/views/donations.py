"""Donations view."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

# Serializers
from apps.donations.serializers import DonationModelSerializer, DonationCreateSerializer

# Models
from apps.donations.models import Donation

# Utils
from apps.utils.mixins import ProjectDispatchMixin


class DonationViewSet(ProjectDispatchMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Donation view set."""

    serializer_class = DonationModelSerializer


    def get_queryset(self):
        return Donation.objects.filter(project=self.project)

    def create(self, request, slug_name):
        """Handle creation."""
        context = {'request': request, 'project': self.project}
        serializer = DonationCreateSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()
        data = self.get_serializer(donation).data
        return Response(data, status=status.HTTP_201_CREATED)
