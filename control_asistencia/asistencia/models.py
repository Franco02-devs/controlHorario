from django.db import models, transaction
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
    
    @staticmethod
    def crear_superasistencias(trabajador):
        # Verificar cuál fue la última asistencia procesada para este trabajador
        ultima_asistencia_procesada = UltimaAsistenciaProcesada.objects.filter(trabajador=trabajador).first()
        ultima_id = ultima_asistencia_procesada.ultima_asistencia_id if ultima_asistencia_procesada else None
        print("hay ultima?")
        print(ultima_id)
        print("hay ultima?")

        # Obtener todas las asistencias del trabajador ordenadas por fecha y hora
        asistencias = Asistencia.objects.filter(trabajador=trabajador).order_by('fecha', 'hora')
        print("lista")
        print(asistencias)
        print("lista")

        # Filtrar las asistencias para comenzar desde la última procesada
        if ultima_id:
            asistencias = asistencias.filter(id__gt=ultima_id)
        print("lista nueva")
        print(asistencias)
        print("lista nueva")

        # Verificar que haya al menos dos registros de entrada/salida
        if len(asistencias) >= 2:
            print("lista nueva long")
            print(len(asistencias))
            print("lista nueva long")

            # Utilizamos un índice para iterar sobre las asistencias en pares
            i = 0
            while i < len(asistencias) - 1:  # Mientras haya al menos una pareja de entrada-salida
                entrada = asistencias[i]
                print("entrada")
                print(entrada)
                print("entrada")
                salida = asistencias[i + 1]
                print("salida")
                print(salida)
                print("salida")
                # Crear la super asistencia
                final_asistencia = FinalAsistencia.objects.create(
                    trabajador=trabajador,
                    entrada=entrada,
                    salida=salida,
                )
                print(final_asistencia)

                # Imprimir el mensaje de éxito
                print(f"SuperAsistencia creada: Trabajador {trabajador.name} | Entrada {entrada.fecha} {entrada.hora} | Salida {salida.fecha} {salida.hora}")

                # Avanzar al siguiente par de entradas/salidas
                i += 2  # Saltar al siguiente par

            # Si el número de asistencias es impar, la última será una entrada sin salida
            if i < len(asistencias):
                ultima_entrada = asistencias[i]
                # Imprimir un mensaje indicando que la entrada no tiene salida
                print(f"Última entrada sin salida registrada: Trabajador {trabajador.name} | Entrada {ultima_entrada.fecha} {ultima_entrada.hora}")

            # El último registro siempre será una salida, si es impar, no se crea ninguna entrada para él.
            ultima_salida = asistencias[i-1]
            print(f"Última salida registrada: Trabajador {trabajador.name} | Salida {ultima_salida.fecha} {ultima_salida.hora}")

            # Actualizar la última asistencia procesada para este trabajador
            ultima_asistencia_procesada, created = UltimaAsistenciaProcesada.objects.get_or_create(trabajador=trabajador)
            ultima_asistencia_procesada.ultima_asistencia_id = asistencias[i-1].id
            ultima_asistencia_procesada.save()

        else:
            print(f"No se pueden crear super asistencias para el trabajador {trabajador.name} ya que no hay suficientes registros.")
                
    @staticmethod
    def obtener_ultima_asistencia_guardada():
        # Obtén la última "super asistencia" registrada
        ultima_super_asistencia = FinalAsistencia.objects.last()
        if ultima_super_asistencia:
            return ultima_super_asistencia
        return None

class FinalAsistencia(models.Model):
    trabajador = models.ForeignKey(Trabajador, related_name='final_asistencias', on_delete=models.CASCADE)
    
    # Relación de uno a uno con Asistencia para la entrada y salida
    entrada = models.OneToOneField(Asistencia, related_name='entrada_asistencia', on_delete=models.CASCADE)
    salida = models.OneToOneField(Asistencia, related_name='salida_asistencia', on_delete=models.CASCADE)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"FinalAsistencia {self.id} - {self.trabajador.name} - {self.entrada.fecha} a {self.salida.fecha}"    
        
class UltimaAsistenciaProcesada(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    ultima_asistencia_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Última Asistencia Procesada: {self.trabajador.name} - ID: {self.ultima_asistencia_id if self.ultima_asistencia_id else 'Ninguna'}"  

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trabajador = models.OneToOneField(Trabajador, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
