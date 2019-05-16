"""Pictures view."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets, mixins, status

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.second_level import IsProjectOwner, ProjectIsNotFinished

# Models
from apps.publications.models import Picture, Publication
from apps.projects.models import Project

# Serializers
from apps.publications.serializers import PictureModelSerializer


class PictureViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = PictureModelSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner, ProjectIsNotFinished]

    def get_queryset(self):
        return Picture.objects.filter(publication=self.publication)

    def dispatch(self, request, *args, **kwargs):
        """Validate project and publication exists."""
        slug_name = kwargs['slug_name']
        self.project = get_object_or_404(Project, slug_name=slug_name)
        pk = kwargs['id']
        self.publication = get_object_or_404(Publication, pk=pk)
        return super(PictureViewSet, self).dispatch(request, *args, **kwargs)

    def get_project(self):
        """Return project in the url."""
        return self.project

    def get_serializer_context(self):
        """Return serializer context."""
        context = super(PictureViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['publication'] = self.publication
        return context
