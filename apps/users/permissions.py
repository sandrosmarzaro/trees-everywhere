from rest_framework import permissions


class IsAccountMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # noqa: ANN001, ANN201, PLR6301
        return obj.users.filter(id=request.user.id).exists()
