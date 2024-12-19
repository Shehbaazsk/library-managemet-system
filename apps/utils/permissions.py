
from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admin.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if hasattr(obj, 'user') and obj.user == request.user:
            return True

        return False


class IsAuthorOrAdmin(BasePermission):
    """
    Custom permission to only allow author of an object or admin.
    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        if request.user.is_superuser:
            return True

        if hasattr(view.get_object(), 'author') and view.get_object().author == request.user:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True

        if request.user.is_superuser:
            return True

        if hasattr(obj, 'author') and obj.author == request.user:
            return True

        return False
