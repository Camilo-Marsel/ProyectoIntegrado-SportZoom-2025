from django.urls import path
from . import views

urlpatterns = [
    # Tareas
    path('tareas/', views.listar_tareas, name='listar_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),

    # Labores
    path('labores/', views.listar_labores, name='listar_labores'),
    path('labores/crear/', views.crear_labor, name='crear_labor'),
    path('labores/editar/<int:pk>/', views.editar_labor, name='editar_labor'),
    path('labores/eliminar/<int:pk>/', views.eliminar_labor, name='eliminar_labor'),
    path('labores/obtener-lotes/', views.obtener_lotes, name='obtener_lotes'),
    path('obtener_lotes_por_finca/<int:finca_id>/', views.obtener_lotes_por_finca, name='obtener_lotes_por_finca'),
    path('obtener_tamano_lote/<int:lote_id>/', views.obtener_tamano_lote, name='obtener_tamano_lote'),
    path('ajax/cargar_trabajadores/', views.cargar_trabajadores, name='cargar_trabajadores'),
]
