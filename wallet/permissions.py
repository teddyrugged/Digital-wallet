from rest_framework import permissions


class IsElite(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_elite)

