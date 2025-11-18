from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend  # NUEVO
from rest_framework import filters  # NUEVO
from .models import Producto, Pedido
from .serializers import ProductoSerializer, AdminLoginSerializer, PedidoSerializer
from .permissions import IsAdminUserCustom
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PedidoSerializer
from rest_framework.decorators import api_view
from django.conf import settings
import requests
import uuid



class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # NUEVO
    filterset_fields = ['marca', 'talla']  # NUEVO
    search_fields = ['nombre']  # NUEVO

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por rango de precio
        precio_min = self.request.query_params.get('precio_min')
        precio_max = self.request.query_params.get('precio_max')
        
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
            
        return queryset


# VISTAS ADMINISTRATIVAS

class ProductoCreate(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUserCustom]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductoUpdate(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUserCustom]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductoDelete(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUserCustom]


class AdminLoginView(APIView):
    """
    Vista para iniciar sesión como administrador.
    Devuelve un token JWT si las credenciales son válidas y el usuario es administrador.
    """
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'es_admin': getattr(user, 'es_admin', False)
        }, status=status.HTTP_200_OK)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # NUEVO
    filterset_fields = ['marca', 'talla']  # NUEVO
    search_fields = ['nombre']  # NUEVO
    
    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserCustom()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por rango de precio
        precio_min = self.request.query_params.get('precio_min')
        precio_max = self.request.query_params.get('precio_max')
        
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        print("FILES:", request.FILES)
        print("POST:", request.data)
        return super().create(request, *args, **kwargs)
    
# Nuevo endpoint para crear pedidos
# ======================================
#  PEDIDOS
# ======================================

@api_view(['POST'])
def crear_pedido(request):
    serializer = PedidoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    pedido = serializer.save()
    return Response({
        "mensaje": "Pedido creado",
        "numero_pedido": pedido.numero_pedido,
        "total": pedido.total
    })

# ======================================
#  PAGO SIMULADO
# ======================================

@api_view(['POST'])
def iniciar_pago(request):
    numero_pedido = request.data.get("numero_pedido")
    nombre = request.data.get("nombre")
    total = request.data.get("total")

    if not numero_pedido or not total:
        return Response({"error": "Datos incompletos"}, status=400)

    try:
        pedido = Pedido.objects.get(numero_pedido=numero_pedido)
    except Pedido.DoesNotExist:
        return Response({"error": "Pedido no encontrado"}, status=404)

    # Simular pago aprobado automáticamente
    pedido.estado = "pagado"
    pedido.save()

    # Devuelve también el carrito
    return Response({
        "mensaje": "Pago aprobado",
        "numero_pedido": pedido.numero_pedido,
        "nombre": pedido.nombre,
        "total": pedido.total,
        "carrito": pedido.carrito
    })

# ======================================
#  VERIFICAR PAGO
# ======================================

@api_view(['GET'])
def verificar_pago(request, numero_pedido):
    try:
        pedido = Pedido.objects.get(numero_pedido=numero_pedido)
    except Pedido.DoesNotExist:
        return Response({"error": "Pedido no existe"}, status=404)

    return Response({
        "estado": pedido.estado
    })