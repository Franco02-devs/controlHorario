from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Trabajador(models.Model):
    
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Asistencia(models.Model):
    
    def obtener_hora_actual():
        return datetime.now().time()
    
    elegirLugar=[('oficina', 'Oficina'),
        ('campo', 'Campo'),]
    elegirTipoRegistro=[('entrada', 'Entrada'),
        ('salida', 'Salida'),]
    esDiferida=False
    
    trabajador=models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    lugar=models.CharField(max_length=10,choices=elegirLugar)
    tipo=models.CharField(max_length=10,choices=elegirTipoRegistro)
    fecha = models.DateField(default=datetime.today)
    hora = models.TimeField(default=obtener_hora_actual)
    foto = models.ImageField(upload_to='fotos_asistencia/')
    fecha_diferida = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.trabajador.name} - {self.tipo} - {self.fecha} {self.hora}"
        

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trabajador = models.OneToOneField(Trabajador, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    
    
    
    
    


