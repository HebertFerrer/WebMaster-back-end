"""User views."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
# from apps.users.filters import UserFilter

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions.users import IsAccountOwner

# Models
from apps.users.models import User

# Serializers
from apps.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer,
    VerifyAccountSerializer,
    UserLoginSerializer,
    ProfileModelSerializer,
    FollowCreateSerializer,
    FollowModelSerializer
)

# Utils
from apps.utils.views import DynamicFieldView


class UserViewSet(DynamicFieldView,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """A viewset that provides login, signup and verification account."""

    serializer_class = UserModelSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'

    # Filters
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter
    )
    ordering_fields = (
        'username',
        'profile__born_date',
        # 'profile__profile_worker__reputation',
        'profile__profile_creator__reputation',
    )
    filterset_fields = (
        'profile__verified',
        # 'profile__profile_worker__reputation',
    )

    # Return dynamic fields
    view_name = 'users'
    fields_to_return = {
        'list': {
            'username': None,
            'phone_number': None,
            'first_name': None,
            'last_name': None,
            'followers': {
                'follower': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'followeds': {
                'followed': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'profile': {
                'picture': None,
                'verified': None,
                'born_date': None,
                'profile_creator': {
                    'reputation': None
                },
                'profile_worker': {
                    'reputation': None
                }
            }
        },
        'retrieve': {
            'username': None,
            'email': None,
            'phone_number': None,
            'first_name': None,
            'last_name': None,
            'followers': {
                'follower': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'followeds': {
                'followed': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'follow_requests': None,
            'profile': {
                'biography': None,
                'gender': None,
                'picture': None,
                'country': None,
                'verified': None,
                'born_date': None,
                'profile_creator': {
                    'reputation': None,
                    'projects': {
                        'title': None,
                        'created': None,
                        'finished': None,
                    }
                },
                'profile_worker': {
                    'reputation': None,
                    'projects': {
                        'title': None,
                        'created': None,
                        'finished': None,
                    }
                }
            }
        },
        'login': {
            'username': None,
            'email': None,
            'phone_number': None,
            'first_name': None,
            'last_name': None,
            'follow_requests': None,
            'followers': {
                'follower': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'followeds': {
                'followed': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'profile': {
                'biography': None,
                'gender': None,
                'picture': None,
                'country': None,
                'verified': None,
                'born_date': None,
                'profile_creator': {
                    'reputation': None,
                    'projects': {
                        'title': None,
                        'created': None,
                        'finished': None,
                    }
                },
                'profile_worker': {
                    'reputation': None,
                    'projects': {
                        'title': None,
                        'created': None,
                        'finished': None,
                    }
                }
            }
        },
        'update': {
            'username': None,
            'email': None,
            'phone_number': None,
            'first_name': None,
            'last_name': None,
            'follow_requests': None,
            'followers': {
                'follower': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'followeds': {
                'followed': {
                    'username': None,
                    'email': None,
                    'phone_number': None,
                    'first_name': None,
                    'last_name': None,
                    'profile': {
                        'gender': None,
                    }
                }
            },
            'profile': {
                'biography': None,
                'gender': None,
                'picture': None,
                'country': None,
                'verified': None,
                'born_date': None,
                'profile_creator': {
                    'reputation': None,
                    'projects': {
                        'title': None,
                        'created': None,
                        'finished': None,
                    }
                },
                'profile_worker': {
                    'reputation': None,
                    'projects': {
                        'title': None,
                        'created': None,
                        'finished': None,
                    }
                }
            }
        },
        'username': {
            'username': None
        },
        'email': {
            'email': None
        },
        'phone': {
            'phone_number': None
        }
    }


    def get_permissions(self):
        """Get permission base on action."""
        permission_classes = []
        if self.action in ['retrieve', 'list']:
            permission_classes.append(IsAuthenticated)
        if self.action in ['update', 'profile']:
            permission_classes.extend([IsAuthenticated, IsAccountOwner])
        return [permission() for permission in permission_classes]

    # Actions
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """Signup action."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'message': 'Now go and verify your account with email.',
            'user': self.get_serializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='verify/(?P<token>[a-zA-Z0-9]+)')
    def verify(self, request, token):
        """Verify accounts."""
        serializer = VerifyAccountSerializer(data={'token':token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations! Now you can login.'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login action."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'token': token,
            'user': self.get_serializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, username):
        """Update profile's information."""
        user = self.get_object()
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            user.profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def username(self, request):
        """Return all usernames."""
        queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def email(self, request):
        """Return all emails."""
        queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def phone_number(self, request):
        """Return all phone numbers."""
        queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
