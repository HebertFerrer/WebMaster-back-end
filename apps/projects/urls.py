"""Project urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework import routers

# Views
from apps.projects import views as project_views

router = routers.DefaultRouter()

# 1rst level
router.register(r'projects', project_views.ProjectViewSet, basename='projects')

# 2nd level

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

router.register(
    r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/publications',
    project_views.PublicationViewSet,
    basename='publications'
)

router.register(
    r'projects/(?P<slug_name>[a-zA-Z0-9-_]+)/publications/(?P<id>[0-9]+)/pictures',
    project_views.PictureViewSet,
    basename='pictures'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
