from django.contrib import admin
from .models import Usuario, Rol, UsuarioRol

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'rol', 'disponibilidad')
    search_fields = ('nombres', 'apellidos', 'user__username')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'asignado_en')
    search_fields = ('usuario__nombres', 'rol__nombre')
