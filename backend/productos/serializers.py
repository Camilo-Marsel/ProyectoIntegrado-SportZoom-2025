from rest_framework import serializers
from .models import Producto

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