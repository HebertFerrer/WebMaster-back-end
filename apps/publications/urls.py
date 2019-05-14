"""Publication urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.publications import views as publication_views

router = DefaultRouter()
router.register(r'publications', publication_views.PublicationViewSet, basename='publications')

router.register(
    r'publications/(?P<id>[0-9]+)/comments',
    publication_views.CommentViewSet,
    basename='comments'
)

router.register(
    r'publications/(?P<id>[0-9]+)/likes',
    publication_views.LikeViewSet,
    basename='likes'
)

urlpatterns = [
    path('', include(router.urls)),
]
