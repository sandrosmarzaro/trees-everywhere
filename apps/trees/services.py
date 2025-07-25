from decimal import Decimal

from django.core.exceptions import PermissionDenied
from django.db import transaction

from apps.users.models import Account, User

from .models import PlantedTree, Tree


@transaction.atomic
def plant_tree(
    user: User,
    account: Account,
    tree: Tree,
    latitude: Decimal,
    longitude: Decimal,
) -> PlantedTree:
    """
    Plants a single tree at a specific location for an account.

    Args:
        user: User logged in.
        tree: Tree instance to be planted.
        location: Tuple (latitude, longitude) as Decimal.
        account: Account associated with the planting.

    Raises:
        PermissionDenied: If the user does not belong to the account.
    """
    if not user.accounts.filter(pk=account.pk).exists():
        raise PermissionDenied(
            'User does not have permission to plant in this account.'
        )

    return PlantedTree.objects.create(
        user=user,
        account=account,
        tree=tree,
        latitude=latitude,
        longitude=longitude,
    )


@transaction.atomic
def plant_trees(
    *, user: User, account: Account, plants: list[dict]
) -> list[PlantedTree]:
    """
    Plants multiple trees at specified locations for an account.

    Args:
        user: User logged in.
        plants: List of tuples, where each tuple contains a `Tree`
        instance and a tuple (latitude, longitude) as `Decimal`.
        account: Account associated with the tree planting.
    Raises:
        PermissionDenied: If the user does not belong to the account.
    """
    if not user.accounts.filter(pk=account.pk).exists():
        raise PermissionDenied(
            'User does not have permission to plant in this account.'
        )

    planted_trees_to_create = [
        PlantedTree(
            user=user,
            account=account,
            tree=plant[0],
            latitude=plant[1][0],
            longitude=plant[1][1],
        )
        for plant in plants
    ]

    return PlantedTree.objects.bulk_create(planted_trees_to_create)
