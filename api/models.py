from __future__ import annotations

import uuid
from datetime import timezone
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models


class Account(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False,
    )
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False,
    )
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
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False,
    )
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
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username}'

    class Meta:
        ordering = ['-joined']


class Tree(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False,
    )
    name = models.CharField(max_length=255, unique=True)
    scientific_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class PlantedTree(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False,
    )
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planted_trees',
    )
    tree = models.ForeignKey(
        Tree, on_delete=models.PROTECT, related_name='plantings'
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='planted_trees'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def age(self) -> int:
        return timezone.now().year - self.planted_at.year

    def clean(self) -> None:
        super().clean()

        MAX_LATITUDE = 90
        MAX_LONGITUDE = 180

        if not (-MAX_LATITUDE <= self.latitude <= MAX_LATITUDE):
            raise ValidationError('Latitude must be between -90 and 90')
        if not (-MAX_LONGITUDE <= self.longitude <= MAX_LONGITUDE):
            raise ValidationError('Longitude must be between -180 and 180.')

        if self.account not in self.user.accounts.all():
            raise PermissionDenied(
                'User does not belong to the selected account.'
            )

    def __str__(self) -> str:
        return f'{self.tree.name} planted by {self.user.username}'

    class Meta:
        ordering = ['-planted_at']
        indexes = [
            models.Index(fields=['user', 'account']),
        ]
