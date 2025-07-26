from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:  # noqa: ANN001, PLR6301
        return obj.user == request.user
