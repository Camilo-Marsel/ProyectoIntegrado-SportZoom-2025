from django.urls import path, include
from .views import ProductoList
from .views import AdminLoginView
#from .views import ProductoDetail
from .views import ProductoCreate
from .views import ProductoUpdate
from .views import ProductoDelete
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),
    path('productos/', ProductoList.as_view(), name='productos-list'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/productos/crear/', ProductoCreate.as_view(), name='producto-create'),
    path('admin/productos/<int:pk>/actualizar/', ProductoUpdate.as_view(), name='producto-update'),
    path('admin/productos/<int:pk>/eliminar/', ProductoDelete.as_view(), name='producto-delete'),
]