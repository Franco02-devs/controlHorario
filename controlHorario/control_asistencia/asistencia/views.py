# views.py
from django.shortcuts import render, redirect
from .forms import AsistenciaForm
from .models import Asistencia
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def registrar_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST, request.FILES)
        if form.is_valid():
            asistencia = form.save(commit=False)
            asistencia.save()
            messages.success(request, '¡Asistencia registrada con éxito!')
            return redirect('registrar_asistencia')  # Redirigir para evitar reenvíos del formulario
    else:
        form = AsistenciaForm()
    return render(request, 'asistencia/registrar_asistencia.html', {'form': form})



@login_required
def vista_admin(request):
    # Vista para el admin que puede ver las asistencias de los trabajadores
    asistencias = Asistencia.objects.all()
    return render(request, 'asistencia/admin_dashboard.html', {'asistencias': asistencias})
