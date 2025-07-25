from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.utils import timezone

from apps.core.fields import UUIDv7Field


class Tree(models.Model):
    id = UUIDv7Field(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    scientific_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class PlantedTree(models.Model):
    id = UUIDv7Field(primary_key=True)
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
        'users.Account', on_delete=models.CASCADE, related_name='planted_trees'
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

        if self.latitude is not None and not (
            -MAX_LATITUDE <= self.latitude <= MAX_LATITUDE
        ):
            raise ValidationError('Latitude must be between -90 and 90')
        if self.longitude is not None and not (
            -MAX_LONGITUDE <= self.longitude <= MAX_LONGITUDE
        ):
            raise ValidationError('Longitude must be between -180 and 180.')

        if hasattr(self, 'user') and hasattr(self, 'account'):
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
