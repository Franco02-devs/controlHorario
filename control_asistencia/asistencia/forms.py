from django import forms
from .models import Asistencia, Trabajador
from django.forms import ModelForm

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['trabajador', 'lugar', 'tipo', 'foto', 'fecha_diferida']
        widgets = {
            'fecha_diferida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), label="Selecciona tu nombre")
    tipo = forms.ChoiceField(choices=Asistencia.elegirTipoRegistro, label="¿Es entrada o salida?")
    lugar = forms.ChoiceField(choices=Asistencia.elegirLugar, label="¿Estás en oficina o en campo?")
    foto = forms.ImageField(label="Sube una foto de la entrada o salida")
    fecha_diferida = forms.DateTimeField(
        required=False,
        label="¿Fuera de tiempo? Registra tu fecha y hora de salida real si es necesario. Fecha Diferida",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )