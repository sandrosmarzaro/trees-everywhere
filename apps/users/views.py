from typing import Type

from django.db.models.query import QuerySet
from rest_framework import serializers, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAuthenticated,
)
from rest_framework.response import Response

from .models import Account, Profile, User
from .permissions import IsAccountMember
from .serializers import (
    AccountMemberSerializer,
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
    ) -> Type[UserSerializer | UserCreateSerializer | AccountMemberSerializer]:
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'add_to_account':
            return AccountMemberSerializer
        return UserSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action == 'add_to_account':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='add-to-account')
    def add_to_account(self, request) -> Response:  # noqa: ANN001, PLR6301
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_id = serializer.validated_data['account_id']

        user = request.user
        account = Account.objects.get(id=account_id)
        user.accounts.add(account)

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAccountMember]

    def get_queryset(self) -> QuerySet[Account]:
        return self.request.user.accounts.all()

    def get_permissions(self) -> list[BasePermission]:
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


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
