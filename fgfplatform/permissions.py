from rest_framework import permissions

class IsEditor(permissions.BasePermission):
    """
    Custom permission to only allow editors to access a particular view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_editor

class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors to access a particular view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_contributor

class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access a particular view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
