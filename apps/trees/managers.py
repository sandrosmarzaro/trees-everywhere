from __future__ import annotations

from django.db import models

from apps.users.models import Account


class PlantedTreeQuerySet(models.QuerySet):
    """Custom QuerySet fro class PlantedTree."""

    def for_user(self, user: models.Model) -> PlantedTreeQuerySet:
        """Return planted trees that belong to user."""
        return self.filter(user=user)

    def for_accounts(self, accounts: list[Account]) -> PlantedTreeQuerySet:
        """Return planted trees whose account is within accounts."""
        return self.filter(account__in=accounts)


class PlantedTreeManager(models.Manager):
    """Manager that exposes PlantedTreeQuerySet helpers."""

    def get_queryset(self) -> PlantedTreeQuerySet:
        return PlantedTreeQuerySet(self.model, using=self._db)

    def for_user(self, user: models.Model) -> PlantedTreeQuerySet:
        return self.get_queryset().for_user(user)

    def for_accounts(self, accounts: list[Account]) -> PlantedTreeQuerySet:
        return self.get_queryset().for_accounts(accounts)
