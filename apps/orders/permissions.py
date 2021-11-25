from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOrderOwner(BasePermission):

    edit_methods = ('PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.user == request.user or obj.shop.user == request.user:
            return True

        return False
