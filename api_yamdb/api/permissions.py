"""
Provides a set of pluggable permission policies.
"""
from rest_framework import permissions


class IsAdminOrAuthenticated(permissions.BasePermission):
    """
    Allows access to admin users,
    or to authenticated users for the methods GET and PATCH.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.role in ["admin"] or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in ["GET"] or request.method in ["PATCH"]
        ) and request.obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows access only to users with the role "admin",
    or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user.role in ["admin"] or request.user.is_superuser)
        )


class ReviewAndComment(permissions.BasePermission):
    """
    Allows create to authenticated users,
    change to owners, moderators, administrators, superusers,
    or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role in ["moderator", "admin"]
            or request.user.is_superuser
            or request.obj == request.user
        )
