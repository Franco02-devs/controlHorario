# views.py
from django.shortcuts import render, redirect
from .forms import AsistenciaForm
from .models import Asistencia, Trabajador
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import timedelta
from .models import Trabajador, Asistencia
import datetime

def exportar_asistencias_a_excel(request):
    # Crea un libro de trabajo de Excel
    wb = Workbook()
    wb.remove(wb.active)  # Eliminar la hoja predeterminada

    # Obtener todos los trabajadores
    trabajadores = Trabajador.objects.all()

    for trabajador in trabajadores:
        # Crear una hoja para cada trabajador
        ws = wb.create_sheet(title=trabajador.name)

        # Establecer los encabezados de la hoja
        ws.append(['Fecha', 'Ingreso', 'Salida', 'Refrigerio/Almuerzo', 'Hora Total'])

        # Obtener las asistencias de ese trabajador
        asistencias = Asistencia.objects.filter(trabajador=trabajador)

        # Poblar las filas con las asistencias
        for asistencia in asistencias:
            # Extraer datos
            fecha = asistencia.fecha
            hora_entrada = asistencia.hora if asistencia.tipo == 'entrada' else None
            hora_salida = asistencia.hora if asistencia.tipo == 'salida' else None
            # Asumimos que si no es salida, se calcula como refrigerio o almuerzo
            refrigerio = ''  # Aquí podrías agregar más lógica según tu modelo o datos
            hora_total = None

            # Si tenemos hora de entrada y salida, calculamos la duración
            if hora_entrada and hora_salida:
                # Calcular la diferencia de horas trabajadas (suponemos 1 hora de almuerzo por ejemplo)
                diferencia = datetime.combine(fecha, hora_salida) - datetime.combine(fecha, hora_entrada)
                hora_total = diferencia - timedelta(hours=1)  # Si hay 1 hora de almuerzo

            # Añadir los datos de la fila
            ws.append([fecha, hora_entrada, hora_salida, refrigerio, hora_total])

        # Autoajustar las columnas
        for col in range(1, 6):
            max_length = 0
            column = get_column_letter(col)
            for row in ws.iter_rows(min_col=col, max_col=col):
                for cell in row:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width

    # Configurar la respuesta para enviar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=asistencias_trabajadores.xlsx'
    wb.save(response)
    return response


def registrar_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST, request.FILES)
        if form.is_valid():
            asistencia = form.save(commit=False)
            asistencia.save()
            messages.success(request, '¡Asistencia registrada con éxito!')
            return redirect('registrar_asistencia') 
    else:
        form = AsistenciaForm()
    return render(request, 'asistencia/registrar_asistencia.html', {'form': form})


#Admin dashboard

@login_required
def vista_admin(request):
    # Vista para el admin que puede ver las asistencias de los trabajadores
    asistencias = Asistencia.objects.all()
    return render(request, 'asistencia/admin/admin_dashboard.html', {'asistencias': asistencias})

@method_decorator(login_required, name='dispatch')
class TrabajadorListView(ListView):
    model = Trabajador
    template_name = 'asistencia/admin/trabajador_list.html'
    context_object_name = 'trabajadores'

@method_decorator(login_required, name='dispatch')
class TrabajadorCreateView(CreateView):
    model = Trabajador
    template_name = 'asistencia/admin/trabajador_form.html'
    fields = ['name']  # Incluye aquí todos los campos que deseas manejar
    success_url = reverse_lazy('trabajador_list')

@method_decorator(login_required, name='dispatch')
class TrabajadorUpdateView(UpdateView):
    model = Trabajador
    template_name = 'asistencia/admin/trabajador_form.html'
    fields = ['name']  # Igual que en CreateView
    success_url = reverse_lazy('trabajador_list')

@method_decorator(login_required, name='dispatch')
class TrabajadorDeleteView(DeleteView):
    model = Trabajador
    template_name = 'asistencia/admin/trabajador_confirm_delete.html'
    success_url = reverse_lazy('trabajador_list')
    

# Vista para el Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# Vista para gestionar asistencias (solo ejemplo)
@login_required
def gestionar_asistencias(request):
    # Aquí agregarías la lógica para gestionar asistencias
    return render(request, 'dashboard/gestionar_asistencias.html')

# Vista para gestionar errores (solo ejemplo)
@login_required
def gestionar_errores(request):
    # Aquí agregarías la lógica para gestionar errores
    return render(request, 'dashboard/gestionar_errores.html')


