from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.fields import UUIDv7Field


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
