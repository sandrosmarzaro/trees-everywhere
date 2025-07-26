from typing import Any

from rest_framework import serializers

from apps.users.serializers import AccountSerializer, UserSerializer

from . import services
from .models import Account, PlantedTree, Tree


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ('id', 'name', 'scientific_name')


class PlantedTreeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tree = TreeSerializer(read_only=True)
    account = AccountSerializer(read_only=True)
    age = serializers.IntegerField(read_only=True)

    tree_id = serializers.PrimaryKeyRelatedField(
        queryset=Tree.objects.all(), source='tree', write_only=True
    )
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.none(), source='account', write_only=True
    )

    class Meta:
        model = PlantedTree
        fields = (
            'id',
            'planted_at',
            'latitude',
            'longitude',
            'age',
            'user',
            'tree',
            'account',
            'tree_id',
            'account_id',
        )
        read_only_fields = ('planted_at', 'age', 'user')

    def __init__(self, *args: tuple, **kwargs: dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['account_id'].queryset = request.user.accounts.all()

    def create(self, validated_data: dict[str, Any]) -> PlantedTree:
        return services.plant_tree(
            user=self.context['request'].user, **validated_data
        )
