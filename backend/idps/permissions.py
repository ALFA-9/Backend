from rest_framework import permissions


class DirectorPermission(permissions.BasePermission):
    """Начальник и сам пользователь имеет доступ."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.employee in request.user.get_descendants(include_self=True)


class CreatorPermission(DirectorPermission):
    """Только создатель ИПР имеет доступ."""

    def has_object_permission(self, request, view, obj):
        return obj.director == request.user
