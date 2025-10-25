from rest_framework import permissions

class IsAdminUserCustom(permissions.BasePermission):
    """Permite acceso solo a usuarios con es_admin=True o is_staff=True"""
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and (
                getattr(user, 'es_admin', False) or getattr(user, 'is_staff', False)
            )
        )
