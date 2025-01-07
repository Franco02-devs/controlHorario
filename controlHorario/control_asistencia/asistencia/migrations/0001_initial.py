# Generated by Django 5.1.4 on 2025-01-07 20:49

import asistencia.models
import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar', models.CharField(choices=[('oficina', 'Oficina'), ('campo', 'Campo')], max_length=10)),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)),
                ('fecha', models.DateField(default=datetime.datetime.today)),
                ('hora', models.TimeField(default=asistencia.models.Asistencia.obtener_hora_actual)),
                ('foto', models.ImageField(upload_to='fotos_asistencia/')),
                ('fecha_diferida', models.DateTimeField(blank=True, null=True)),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asistencia.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trabajador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='asistencia.trabajador')),
            ],
        ),
    ]
