from django.test import TestCase

# Create your tests here.
from asistencia.models import Trabajador, Asistencia,FinalAsistencia

trabajadores=Trabajador.objects.all()
trabajador=trabajadores[0]
Asistencia.crear_superasistencias(trabajador)

# Buscar el objeto por su id
dele = FinalAsistencia.objects.get(id=1)

# Eliminar el objeto
producto.delete()

print(f"Producto {producto.nombre} eliminado.")
