from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer

class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer