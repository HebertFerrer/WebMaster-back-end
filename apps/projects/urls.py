"""Project urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework import routers

# Views
from apps.projects import views as project_views

router = routers.DefaultRouter()
router.register(r'projects', project_views.ProjectViewSet, basename='projects')
# router.register(
#     r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/activities',
#     project_views.ActivityViewSet,
#     basename='activities'
# )
router.register(
    r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/jobs',
    project_views.WorkerViewSet,
    basename='jobs'
)
router.register(
    r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/applications',
    project_views.ApplicationViewSet,
    basename='applications'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
