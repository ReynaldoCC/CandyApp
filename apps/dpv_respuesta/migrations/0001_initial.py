# Generated by Django 2.2 on 2020-01-17 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dpv_nomencladores', '0005_auto_20200111_0037'),
        ('dpv_perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='dpv_perfil.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_respuesta', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Respuesta')),
                ('rechazada', models.DateTimeField(default=None, null=True)),
                ('codigo', models.CharField(max_length=14, verbose_name='Código de la Respuesta')),
                ('texto', models.TextField(blank=True, default='', max_length=1000, verbose_name='Texto de la Respuesta')),
                ('clasificacion', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dpv_nomencladores.ClasificacionRespuesta', verbose_name='Clasificación de la Respuesta')),
                ('responde', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='dpv_respuesta.Tecnico')),
            ],
            options={
                'verbose_name': 'Respuesta',
                'verbose_name_plural': 'RespuestaS',
            },
        ),
        migrations.CreateModel(
            name='ApruebaJefe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion_jefe', models.TextField(blank=True, default='', max_length=1000, verbose_name='Observaciones')),
                ('fecha_jefe', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha Aprobación Jefe')),
                ('aprobada_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_perfil.Perfil')),
                ('respuesta', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dpv_respuesta.Respuesta', verbose_name='Respuesta Dada')),
            ],
            options={
                'verbose_name': 'Respuesta Aprobada por Jefe',
                'verbose_name_plural': 'Respuestas Aprobadas por Jefe',
            },
        ),
        migrations.CreateModel(
            name='ApruebaDtr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion_dtr', models.TextField(blank=True, default='', max_length=1000, verbose_name='Observaciones')),
                ('fecha_dtr', models.DateTimeField(blank=True, default='', null=True, verbose_name='Fecha Aprobación Director')),
                ('aprobada_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_perfil.Perfil')),
                ('respuesta', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dpv_respuesta.Respuesta', verbose_name='Respuesta Dada')),
            ],
            options={
                'verbose_name': 'Respuesta Aprobada por Director',
                'verbose_name_plural': 'Respuestas Aprobadas por Director',
            },
        ),
    ]
