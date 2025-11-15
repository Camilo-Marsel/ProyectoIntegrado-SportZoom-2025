from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend  # NUEVO
from rest_framework import filters  # NUEVO
from .models import Producto
from .serializers import ProductoSerializer, AdminLoginSerializer
from .permissions import IsAdminUserCustom
from rest_framework.parsers import MultiPartParser, FormParser


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