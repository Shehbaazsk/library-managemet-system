
from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    Custom permission to only allow author of an object or admin.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if hasattr(obj, 'author') and obj.author.user == request.user:
            return True

        return False
