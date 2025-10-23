from rest_framework import serializers
from .models import Producto
from django.contrib.auth import authenticate

class ProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField(read_only=True)
    disponibilidad = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'imagen_url', 'disponibilidad']
        extra_kwargs = {
            'imagen': {'required': False, 'allow_null': True },
        }
        

    def get_imagen_url(self, obj):
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