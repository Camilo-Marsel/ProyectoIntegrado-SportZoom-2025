from rest_framework import permissions

class IsAdminUserCustom(permissions.BasePermission):
    """Permite acceso solo a usuarios con es_admin=True"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'es_admin', False))

