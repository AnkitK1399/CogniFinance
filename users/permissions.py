from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsAnalystRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ANALYST'


class IsOwnerAdminOrAnalystReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if obj == request.user:
            return True
        if request.user.role == 'ANALYST' and request.method == 'GET':
            return True
        return False