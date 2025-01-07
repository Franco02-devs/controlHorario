# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('admin/', views.vista_admin, name='vista_admin'),
]
