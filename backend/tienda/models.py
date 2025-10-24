from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    Permite agregar campos adicionales sin perder la estructura base de Django.
    """
    es_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tienda_usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Producto(models.Model):
    """
    Modelo de productos disponibles en la tienda.
    Incluye información básica y una imagen opcional.
    """
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tienda_producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

   
