from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    
    edit_methods = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.posted_by == request.user:
            return True

        return False