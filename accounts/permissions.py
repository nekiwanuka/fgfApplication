from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Allow superusers full access to all views.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and a superuser
        return request.user.is_authenticated and request.user.is_superuser

class IsEditorOrSuperUser(permissions.BasePermission):
    """
    Allow editors and superusers to perform CRUD operations.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and either an editor or superuser
        return request.user.is_authenticated and (request.user.is_editor or request.user.is_superuser)

class IsContributor(permissions.BasePermission):
    """
    Allow contributors to create new suggestions but not modify existing entries.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and a contributor
        return request.user.is_authenticated and request.user.is_contributor

    def has_object_permission(self, request, view, obj):
        # Contributors can view and submit new entries, but can't update or delete existing entries
        if request.method in ['GET', 'POST']:
            return True
        return False

class ReadOnlyOrEditorSuperUser(permissions.BasePermission):
    """
    Allow read-only access for authenticated users and CRUD access for editors and superusers.
    """
    def has_permission(self, request, view):
        # Require authentication for all requests
        if request.user.is_authenticated:
            # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                return True
            # Allow CRUD access for editors and superusers
            return request.user.is_editor or request.user.is_superuser
        return False

class IsViewerOrSuperUser(permissions.BasePermission):
    """
    Allow viewers and superusers to view content.
    """
    def has_permission(self, request, view):
        # Require authentication for all requests
        if request.user.is_authenticated:
            return request.user.is_viewer or request.user.is_superuser
        return False

class IsContributorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated contributors to post and get, but not update or delete.
    Also ensures contributors cannot modify fields like 'status'.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow POST requests for authenticated users (contributors)
        if request.method == 'POST' and request.user.is_contributor:
            return True

        # Allow full access for editors and superusers
        if request.user.is_superuser or request.user.groups.filter(name='Editors').exists():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow full access for editors and superusers
        if request.user.is_superuser or request.user.groups.filter(name='Editors').exists():
            return True

        # Deny access for contributors to modify existing entries (PUT, PATCH, DELETE)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return False

        # Allow POST and GET methods for contributors to create and view content
        return True
