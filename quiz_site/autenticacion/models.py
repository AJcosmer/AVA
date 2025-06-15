from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Rol(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Usuario(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    promedio = models.FloatField(null=True, blank=True)
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='roles_asignados')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios_asignados')
    asignado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'rol']
