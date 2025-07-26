from typing import Type

from django.db.models.query import QuerySet
from rest_framework import serializers, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAuthenticated,
)

from .models import Account, Profile, User
from .serializers import (
    AccountSerializer,
    AuthTokenSerializer,
    ProfileSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(
        self,
    ) -> Type[UserSerializer | UserCreateSerializer]:
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Profile]:
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer: ProfileSerializer) -> None:
        if Profile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError('You can only have one profile.')
        serializer.save(user=self.request.user)
