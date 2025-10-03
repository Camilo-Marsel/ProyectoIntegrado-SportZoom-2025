from rest_framework import serializers
from .models import Producto
from django.contrib.auth import authenticate

class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField()
    disponibilidad = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'imagen', 'disponibilidad']

    def get_imagen(self, obj):
        request = self.context.get('request')
        if obj.imagen:
            url = obj.imagen.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_disponibilidad(self, obj):
        return 'Disponible' if obj.stock > 0 else 'Agotado'

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Usuario o contraseña incorrectos')
        if not user.es_admin:
            raise serializers.ValidationError('No tienes permisos de administrador')
        data['user'] = user
        return data