# Generated by Django 2.2.2 on 2020-07-11 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_documento', '0004_tipodpvdocumento_dias_proceso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipodpvdocumento',
            name='dias_proceso',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Días para procesar'),
        ),
    ]
