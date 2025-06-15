from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        perfil = getattr(request.user, 'perfil', None)
        return perfil and perfil.rol and perfil.rol.nombre.lower() in ['admin', 'administrador']
