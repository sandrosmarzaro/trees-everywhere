from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Account, Profile, User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data: dict[str, Any]) -> User:  # noqa: PLR6301
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'accounts')


class AccountMemberSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()

    def validate_account_id(self, value: str) -> str:  # noqa: PLR6301
        if not Account.objects.filter(id=value).exists():
            raise serializers.ValidationError('Account not found.')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'about', 'joined')
        read_only_fields = ('joined', 'user')

    def create(self, validated_data: dict[str, Any]) -> Profile:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password,
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
