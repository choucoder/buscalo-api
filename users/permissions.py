from rest_framework import permissions


class IsAllowedUser(permissions.BasePermission):
    
    edit_methods = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj == request.user:
            return True

        return False