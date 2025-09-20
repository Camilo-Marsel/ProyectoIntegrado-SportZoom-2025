from django.db import models
from personal.models import Trabajador
from fincas.models import Lote  # importante importar desde nueva app


 #--------------------Tarea-----------------------------------------------

class Tarea(models.Model):
    FORMAS_MEDICION = [
        ('día', 'Por día'),
        ('hectarea', 'Por hectárea'),
        ('metro', 'Por metro'),
        ('unidad', 'Por unidad'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    forma_medicion = models.CharField(max_length=13, choices=FORMAS_MEDICION)
    valor_unitario = models.DecimalField(max_digits=11, decimal_places=2)  # valor por unidad, día, etc.

    def __str__(self):
        return f"{self.nombre} ({self.forma_medicion})"


#-------------------------Labor------------------------------------------------
from fincas.models import Finca

class Labor(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT)
    fecha = models.DateField()
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, null=True, blank=True)  # 👈 nuevo campo
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=4)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    observaciones = models.TextField(blank=True)
    nomina_asociada = models.ForeignKey('nomina.Nomina', on_delete=models.SET_NULL, null=True, blank=True, related_name='labores')

    def save(self, *args, **kwargs):
        self.valor_total = self.cantidad * self.tarea.valor_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tarea.nombre} - {self.trabajador} - {self.fecha}"

    

   
