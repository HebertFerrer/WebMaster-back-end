"""Calification urls."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.califications import views as calification_views


router = DefaultRouter()

router.register(
    r'workers/(?P<id>[0-9]+)/califications',
    calification_views.CalificationToWorkerViewSet,
    basename='workers'
)

router.register(
    r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/califications',
    calification_views.CalificationToProjectViewSet,
    basename='projects'
)

router.register(
    r'creators/(?P<id>[0-9]+)/califications',
    calification_views.CalificationToProjectViewSet,
    basename='creators'
)

urlpatterns = [
    path('', include(router.urls))
]
