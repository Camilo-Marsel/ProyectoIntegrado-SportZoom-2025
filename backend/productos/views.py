from django.shortcuts import render, redirect, get_object_or_404
from .models import Labor, Tarea
from .forms import LaborForm, TareaForm  # Necesitarás crear este formulario en forms.py

def listar_labores(request):
    labores = Labor.objects.select_related('trabajador', 'lote').all()
    return render(request, 'labores/listar_labores.html', {'labores': labores})

def detalle_labor(request, pk):
    labor = get_object_or_404(Labor, pk=pk)
    return render(request, 'labores/labor_detail.html', {'labor': labor})
from django.contrib import messages
from datetime import datetime
from .models import Labor
from .forms import LaborForm

def crear_labor(request):
    if request.method == 'POST':
        form = LaborForm(request.POST)
        fechas_str = request.POST.get('fechas_seleccionadas', '')

        if form.is_valid() and fechas_str:
            fechas = fechas_str.split(',')
            creadas = 0
            duplicadas = 0

            for fecha_str in fechas:
                try:
                    fecha = datetime.strptime(fecha_str.strip(), "%Y-%m-%d").date()
                except ValueError:
                    continue

                # Verificar duplicados
                existe = Labor.objects.filter(
                    trabajador=form.cleaned_data['trabajador'],
                    tarea=form.cleaned_data['tarea'],
                    finca=form.cleaned_data['finca'],
                    lote=form.cleaned_data['lote'],
                    fecha=fecha
                ).exists()

                if not existe:
                    Labor.objects.create(
                        trabajador=form.cleaned_data['trabajador'],
                        tarea=form.cleaned_data['tarea'],
                        finca=form.cleaned_data['finca'],
                        lote=form.cleaned_data['lote'],
                        fecha=fecha,
                        cantidad=form.cleaned_data['cantidad'],
                        observaciones=form.cleaned_data['observaciones']
                    )
                    creadas += 1
                else:
                    duplicadas += 1

            if creadas > 0:
                messages.success(request, f"Se crearon {creadas} labores.")
            if duplicadas > 0:
                messages.warning(request, f"{duplicadas} fechas fueron ignoradas por estar duplicadas.")

            return redirect('listar_labores')
    else:
        form = LaborForm()

    return render(request, 'labores/crear_labor.html', {'form': form})

def editar_labor(request, pk):
    labor = get_object_or_404(Labor, pk=pk)
    form = LaborForm(request.POST or None, instance=labor)
    if form.is_valid():
        form.save()
        return redirect('listar_labores')
    return render(request, 'labores/editar_labor.html', {'form': form})

def eliminar_labor(request, pk):
    labor = get_object_or_404(Labor, pk=pk)
    if request.method == 'POST':
        labor.delete()
        return redirect('listar_labores')
    return render(request, 'labores/eliminar_labor.html', {'labor': labor})

from django.http import JsonResponse
from fincas.models import Lote
from django.http import JsonResponse
from .models import Lote

def obtener_lotes_por_finca(request, finca_id):
    lotes = Lote.objects.filter(finca_id=finca_id).values('id', 'nombre')
    return JsonResponse(list(lotes), safe=False)

def obtener_tamano_lote(request, lote_id):
    lote = Lote.objects.filter(id=lote_id).first()
    return JsonResponse({'tamano': str(lote.tamaño_m2) if lote else ""})

def obtener_lotes(request):
    finca_id = request.GET.get('finca_id')
    lotes = Lote.objects.filter(finca_id=finca_id).values('id', 'nombre', 'tamano')
    return JsonResponse({'lotes': list(lotes)})

#
from django.http import JsonResponse
from .models import Trabajador

def cargar_trabajadores(request):
    finca_id = request.GET.get('finca')
    trabajadores = Trabajador.objects.filter(finca_id=finca_id).order_by('nombre_completo')
    data = [{'id': t.id, 'nombre': f"{t.nombre_completo} ({t.numero_documento})"} for t in trabajadores]
    return JsonResponse(data, safe=False)


### TAREAS ###
def listar_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas/listar_tareas.html', {'tareas': tareas})

def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/crear_tarea.html', {'form': form})

def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    form = TareaForm(request.POST or None, instance=tarea)
    if form.is_valid():
        form.save()
        return redirect('listar_tareas')
    return render(request, 'tareas/editar_tarea.html', {'form': form})

def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('listar_tareas')
    return render(request, 'tareas/eliminar_tarea.html', {'tarea': tarea})