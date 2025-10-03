from django.urls import path
from .views import ProductoList
from .views import AdminLoginView

urlpatterns = [
    path('productos/', ProductoList.as_view(), name='productos-list'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
]