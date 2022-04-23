from rest_framework import permissions
from authentication.models import User


class AdminOrAuthenticatedReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return (bool(request.user and request.user.is_authenticated) and request.method == "GET") or bool(request.user and request.user.is_staff)

# class OwnerOrReadOnly(permissions.BasePermission):
#      def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         else:
#             return obj.username_id == request.user
