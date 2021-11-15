from rest_framework import permissions


class IsShopOwner(permissions.BasePermission):

    edit_methods = ('PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.user == request.user:
            return True

        return False