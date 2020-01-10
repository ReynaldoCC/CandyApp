# Generated by Django 2.1 on 2019-04-10 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_complaint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accepted',
            name='answer',
            field=models.CharField(choices=[('Trámite', 'Trámite'), ('PR', 'Pendiente de Respuesta'), ('S', 'Solución o Resuelto'), ('PS', 'Pendiente de Solución'), ('ECNS', 'Explicada Causa de no Solución')], default='S', max_length=100),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('Pendiente', 'P'), ('Esperando Asignación', 'EA'), ('Esperando Respuesta de Técnico', 'ERT'), ('Esperando aceptación del jefe', 'EAJ'), ('Finalizada', 'F')], default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='currentcomplaint',
            name='current_status',
            field=models.CharField(choices=[('Esperando aceptación del jefe', 'Esperando aceptación del jefe'), ('Finalizada', 'Finalizada'), ('Esperando Asignación', 'Esperando Asignación'), ('Pendiente', 'Pendiente'), ('Esperando Respuesta de Técnico', 'Esperando Respuesta de Técnico')], default='Pendiente', max_length=100),
        ),
        migrations.AlterField(
            model_name='historycomplaint',
            name='boss_answer',
            field=models.CharField(blank=True, choices=[('Trámite', 'Trámite'), ('PR', 'Pendiente de Respuesta'), ('S', 'Solución o Resuelto'), ('PS', 'Pendiente de Solución'), ('ECNS', 'Explicada Causa de no Solución')], default='S', max_length=20),
        ),
        migrations.AlterField(
            model_name='historycomplaint',
            name='current_status',
            field=models.CharField(choices=[('Esperando aceptación del jefe', 'Esperando aceptación del jefe'), ('Finalizada', 'Finalizada'), ('Esperando Asignación', 'Esperando Asignación'), ('Pendiente', 'Pendiente'), ('Esperando Respuesta de Técnico', 'Esperando Respuesta de Técnico')], default='Pendiente', max_length=200),
        ),
    ]
