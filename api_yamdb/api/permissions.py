'''
Provides a set of pluggable permission policies.
'''
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    '''
    Allows access to admin users.
    '''

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsSelf(permissions.BasePermission):
    '''
    Allow to access their account.
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in ['GET', 'PATCH'] and obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    Allows access only to users with the role 'admin',
    or is a read-only request.
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class ReviewAndComment(permissions.BasePermission):
    '''
    Allows create to authenticated users,
    change to owners, moderators, administrators, superusers,
    or is a read-only request.
    '''

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or obj.author == request.user
        )
