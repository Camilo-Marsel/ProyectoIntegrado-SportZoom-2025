from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    es_admin = models.BooleanField(default=False)


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    talla = models.CharField(max_length=10, blank=True, null=True)  # Nuevo campo para filtros
    marca = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo para filtros
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

    class Meta:
        db_table = 'tienda_producto'

    

   
