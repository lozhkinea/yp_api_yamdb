from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
            )

    def has_object_permission(self, request, view, obj):
        return (request.user.role == "admin"
            )
