from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """Allow superusers full access to all views."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsEditorOrSuperUser(permissions.BasePermission):
    """Allow editors and superusers to have full access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_editor)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_editor

class IsContributor(permissions.BasePermission):
    """Allow contributors to create new suggestions but not modify existing entries."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_contributor

    def has_object_permission(self, request, view, obj):
        return request.method in ['GET', 'POST']  # Contributors can only GET and POST

class ReadOnlyOrEditorSuperUser(permissions.BasePermission):
    """Allow read-only access for all users, but CRUD for editors and superusers."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Read-only access
            return True
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_editor)

class IsViewerOrSuperUser(permissions.BasePermission):
    """Allow only viewers and superusers to view content."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_viewer)

class IsContributorOrReadOnly(permissions.BasePermission):
    """Allow contributors to create new content but restrict modification."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Read-only access
            return True
        return request.user.is_authenticated and (
            request.user.is_contributor or request.user.is_superuser or request.user.is_editor
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access
        if request.user.is_superuser or request.user.is_editor:
            return True  # Allow CRUD for editors and superusers
        if request.user.is_contributor and request.method in ['POST']:
            return True  # Contributors can only create
        return False  # Deny modifications for contributors
