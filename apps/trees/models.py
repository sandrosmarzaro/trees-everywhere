from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.fields import UUIDv7Field

from .managers import PlantedTreeManager
from .validators import validate_latitude, validate_longitude


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
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_latitude],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_longitude],
    )

    objects = PlantedTreeManager()

    @property
    def age(self) -> int:
        return timezone.now().year - self.planted_at.year

    def __str__(self) -> str:
        return f'{self.tree.name} planted by {self.user.username}'

    class Meta:
        ordering = ['-planted_at']
        indexes = [
            models.Index(fields=['user', 'account']),
        ]
