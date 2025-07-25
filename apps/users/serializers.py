from typing import Any

from rest_framework import serializers

from .models import Account, Profile, User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'about', 'joined')
        read_only_fields = ('joined', 'user')

    def create(self, validated_data: dict[str, Any]) -> Profile:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
