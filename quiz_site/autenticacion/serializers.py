from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Usuario, Rol, UsuarioRol

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'nombres', 'apellidos', 'promedio', 'disponibilidad']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = User.objects.create_user(username=username, password=password, email=email)

        rol, _ = Rol.objects.get_or_create(nombre='Usuario')
        usuario = Usuario.objects.create(user=user, rol=rol, **validated_data)
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'nombres', 'apellidos', 'promedio', 'disponibilidad', 'rol', 'rol_nombre', 'roles']

    def get_roles(self, obj):
        return [{"id": r.rol.id, "nombre": r.rol.nombre} for r in obj.roles_asignados.select_related('rol')]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']

class UsuarioRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRol
        fields = ['id', 'usuario', 'rol', 'asignado_en']
