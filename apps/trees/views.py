from __future__ import annotations

from django.db.models import QuerySet
from rest_framework import generics, permissions

from apps.core.permissions import IsOwner

from .models import PlantedTree, Tree
from .serializers import (
    PlantedTreeListSerializer,
    PlantedTreeSerializer,
    TreeSerializer,
)


class PlantedTreeListByUserAPIView(generics.ListAPIView):
    serializer_class = PlantedTreeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[PlantedTree]:
        return PlantedTree.objects.for_user(self.request.user).select_related(
            'user', 'tree', 'account'
        )


class PlantedTreeAPIView(generics.RetrieveAPIView):
    serializer_class = PlantedTreeSerializer
    queryset = PlantedTree.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class PlantedTreeCreateAPIView(generics.CreateAPIView):
    serializer_class = PlantedTreeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlantedTreeBulkCreateAPIView(generics.CreateAPIView):
    serializer_class = PlantedTreeListSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlantedTreeListByAccountsAPIView(generics.ListAPIView):
    serializer_class = PlantedTreeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[PlantedTree]:
        user = self.request.user
        user_accounts = user.accounts.all()
        return PlantedTree.objects.for_accounts(user_accounts).select_related(
            'user', 'tree', 'account'
        )


class TreeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TreeSerializer
    queryset = Tree.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class TreeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TreeSerializer
    queryset = Tree.objects.all()
    permission_classes = [permissions.IsAuthenticated]
