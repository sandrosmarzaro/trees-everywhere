from typing import Any

from rest_framework import serializers

from apps.users.models import Account
from apps.users.serializers import AccountSerializer, UserSerializer

from . import services
from .models import PlantedTree, Tree


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


class PlantedTreeItemSerializer(serializers.Serializer):
    tree = TreeSerializer(write_only=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)


class PlantedTreeListSerializer(serializers.Serializer):
    plants = PlantedTreeItemSerializer(many=True)
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.none(), write_only=True
    )

    def __init__(self, *args: tuple, **kwargs: dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['account_id'].queryset = request.user.accounts.all()

    def create(self, validated_data: dict[str, Any]) -> list[PlantedTree]:
        account = validated_data['account_id']
        plants_data = validated_data['plants']

        plants_list = [
            (
                plant_data['tree'],
                (plant_data['latitude'], plant_data['longitude']),
            )
            for plant_data in plants_data
        ]

        user = self.context['request'].user
        return services.plant_trees(
            user=user, account=account, plants=plants_list
        )
