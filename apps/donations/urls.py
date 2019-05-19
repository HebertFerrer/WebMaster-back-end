"""Donation urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.donations import views as donation_views

router = DefaultRouter()
router.register(
    r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/donations',
    donation_views.DonationViewSet,
    basename='donations'
)

urlpatterns = [
    path('', include(router.urls))
]
