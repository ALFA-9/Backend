from rest_framework import permissions


class DirectorPermission(permissions.BasePermission):
    """Только владелец может редактировать свой профиль."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.employee in request.user.get_descendants(include_self=True)
