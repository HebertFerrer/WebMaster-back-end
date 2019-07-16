"""Project views."""

# Django
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Serializers
from apps.projects.serializers import (
    ProjectModelSerializer,
    ProjectCreateSerializer
)

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.projects.permissions.projects import IsProjectOwner, ProjectIsNotFinished

# Models
from apps.projects.models import Project
from apps.donations.models import Donation

# Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

# Utils
from apps.utils.views import DynamicFieldView


class ProjectViewSet(DynamicFieldView,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Project view set."""

    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()
    lookup_field = 'slug_name'

    # Filters
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter
    )
    ordering_fields = (
        'title',
        'costs',
        'amount',
        # Just to filter
        'filter_amount',
        'publication_likes',
        # 'profile__profile_worker__reputation',
        # 'profile__profile_creator__reputation',
    )
    filterset_fields = (
        # 'profile__verified',
        # 'profile__profile_worker__reputation',
    )

    # Return dynamic fields
    view_name = 'projects'
    fields_to_return = {
        'list': (
            'title', 'slug_name', 'description', 'finished',
            'cost', 'reputation', 'category', 'amount', 'creator',
        ),
        'likesTop': (
            'title', 'slug_name', 'description', 'cost',
            'reputation', 'category', 'publication_likes', 'created',
        ),
        'donationsTop': (
            'title', 'slug_name', 'description', 'cost',
            'reputation', 'category', 'filter_amount', 'created',
        ),
        'donationsDown': (
            'title', 'slug_name', 'description', 'cost',
            'reputation', 'category', 'filter_amount', 'created',
        ),
        'likesDown': (
            'title', 'slug_name', 'description', 'cost',
            'reputation', 'category', 'publication_likes', 'created',
        ),
        'retrieve': {
            'title': None,
            'slug_name': None,
            'description': None,
            'cost': None,
            'reputation': None,
            'amount': None,
            'donations': None,
            'category': None,
            'calified': None,
            'creator': None,
            'califications': None,
            'finished': None,
            'created': None,
            'workers': {
                'id': None,
                'worker': {
                    'username': None,
                    'profile': {
                        'picture': None,
                        'profile_worker': {
                            'reputation': None,
                            'position': None
                        }
                    }
                },
                'position': None
            },
            'jobs': {
                'id': None,
                'position': None,
                'created': None
            },
            'publications': {
                'id': None,
                'user': None,
                'description': None,
                'comments': None,
                'likes': None,
                'liked': None,
                'project': None,
                'pictures': {
                    'id': None,
                    'picture': None
                },
                'created': None,
                'updated': None,
            }
        }
    }

    def get_permissions(self):
        """Get permissions base on action."""
        permission_classes = [IsAuthenticated]
        if self.action in ['update', 'finish']:
            permission_classes.extend([IsProjectOwner, ProjectIsNotFinished])
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Handle project creation."""
        serializer = ProjectCreateSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        data = ProjectModelSerializer(project).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def finish(self, request, slug_name):
        """Finish a project."""
        instance = get_object_or_404(Project, slug_name=slug_name)
        serializer = self.get_serializer(
            instance, data={'finished': True}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def donationsTop(self, request):
        """Return donations amount."""
        queryset = Project.objects.filter(
            creator=request.user, finished=False).annotate(filter_amount=Sum(
            'donation__amount')).order_by('-filter_amount')[:5]
        serializer = self.get_serializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def likesTop(self, request):
        """Return donations amount."""
        queryset = Project.objects.filter(creator=request.user, finished=False).annotate(
            publication_likes=Count('publication__liketopublication')).order_by('-publication_likes')[:5]
        serializer = self.get_serializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def donationsDown(self, request):
        """Return donations amount."""
        queryset = Project.objects.filter(
            creator=request.user, finished=False).annotate(filter_amount=Sum(
            'donation__amount')).order_by('filter_amount')[:5]
        serializer = self.get_serializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def likesDown(self, request):
        """Return donations amount."""
        queryset = Project.objects.filter(creator=request.user, finished=False).annotate(
            publication_likes=Count('publication__liketopublication')).order_by('publication_likes')[:5]
        serializer = self.get_serializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
