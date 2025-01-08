# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('admin/', views.vista_admin, name='vista_admin'),
    path('trabajadores/', views.TrabajadorListView.as_view(), name='trabajador_list'),
    path('trabajadores/nuevo/', views.TrabajadorCreateView.as_view(), name='trabajador_create'),
    path('trabajadores/editar/<int:pk>/', views.TrabajadorUpdateView.as_view(), name='trabajador_update'),
    path('trabajadores/eliminar/<int:pk>/', views.TrabajadorDeleteView.as_view(), name='trabajador_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('gestionar-asistencias/', views.gestionar_asistencias, name='gestionar_asistencias'),
    path('gestionar-errores/', views.gestionar_errores, name='gestionar_errores'),
    path('exportar_asistencias/', views.exportar_asistencias_a_excel, name='exportar_asistencias'),

]
