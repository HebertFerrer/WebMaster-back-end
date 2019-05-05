"""Project urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework import routers

# Views
from apps.projects import views as project_views

router = routers.DefaultRouter()
router.register(r'projects', project_views.ProjectViewSet, basename='projects')

urlpatterns = [
    path(r'', include(router.urls)),
]
