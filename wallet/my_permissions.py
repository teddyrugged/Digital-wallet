from rest_framework import permissions


class IsElite(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        print('Is Elite', request.user.username)
        return request.user.is_elite
