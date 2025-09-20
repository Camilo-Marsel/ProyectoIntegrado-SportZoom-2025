from django.contrib import admin
from .models import Labor, Tarea

@admin.register(Labor)
class LaborAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'trabajador', 'get_tarea', 'get_forma_medicion', 'cantidad', 'valor_total', 'lote')
    list_filter = ('fecha', 'trabajador', 'tarea')
    search_fields = ('trabajador__nombres', 'tarea__nombre', 'lote__nombre')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

    def get_tarea(self, obj):
        return obj.tarea.nombre
    get_tarea.short_description = 'Tarea'

    def get_forma_medicion(self, obj):
        return obj.tarea.get_forma_medicion_display()
    get_forma_medicion.short_description = 'Medición'

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'forma_medicion', 'valor_unitario')
    list_filter = ('forma_medicion',)
    search_fields = ('nombre',)
