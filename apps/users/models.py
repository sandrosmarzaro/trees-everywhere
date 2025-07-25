from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.fields import UUIDv7Field
from apps.trees.models import PlantedTree, Tree


class Account(models.Model):
    id = UUIDv7Field(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class User(AbstractUser):
    id = UUIDv7Field(primary_key=True)
    accounts = models.ManyToManyField(
        Account,
        blank=True,
        related_name='users',
        through='UserAccount',
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['username']

    def plant_tree(
        self,
        tree: Tree,
        location: tuple[Decimal, Decimal],
        account: Account,
    ) -> None:
        """
        Plants a single tree at a specific location for an account.

        Args:
            tree: Tree instance to be planted.
            location: Tuple (latitude, longitude) as Decimal.
            account: Account associated with the planting.

        Raises:
            PermissionDenied: If the user does not belong to the account.
        """

        PlantedTree(
            user=self,
            tree=tree,
            account=account,
            latitude=location[0],
            longitude=location[1],
        ).save()

    def plant_trees(
        self,
        plants: list[tuple[Tree, tuple[Decimal, Decimal]]],
        account: Account,
    ) -> None:
        """
        Plants multiple trees at specified locations for an account.

        Args:
            plants: List of tuples, where each tuple contains a `Tree`
            instance and a tuple (latitude, longitude) as `Decimal`.
            account: Account associated with the tree planting.
        Raises:
            PermissionDenied: If the user does not belong to the account.
        """

        planted_trees_to_create = [
            PlantedTree(
                user=self,
                tree=plant[0],
                account=account,
                latitude=plant[1][0],
                longitude=plant[1][1],
            )
            for plant in plants
        ]
        PlantedTree.objects.bulk_create(planted_trees_to_create)


class UserAccount(models.Model):
    id = UUIDv7Field(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} in {self.account.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'account'], name='unique_user_account'
            )
        ]
        ordering = ['-joined_at']


class Profile(models.Model):
    id = UUIDv7Field(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username}'

    class Meta:
        ordering = ['-joined']
