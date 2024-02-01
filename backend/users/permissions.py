from rest_framework import permissions


class UserIsDirectorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj in request.user.get_descendants(include_self=True)
