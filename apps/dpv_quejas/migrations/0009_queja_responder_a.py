# Generated by Django 2.2.2 on 2020-02-05 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_nomencladores', '0011_respuestaaqueja'),
        ('dpv_quejas', '0008_auto_20200127_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='queja',
            name='responder_a',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dpv_nomencladores.RespuestaAQueja', verbose_name='Ofrecer respuesta a'),
        ),
    ]