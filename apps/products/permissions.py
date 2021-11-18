from rest_framework import permissions
from apps.shops.models import Shop


class IsProductOwner(permissions.BasePermission):

    edit_method = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True

        shops = Shop.objects.filter(user=request.user)

        if obj.shop in shops:
            return True

        return False
