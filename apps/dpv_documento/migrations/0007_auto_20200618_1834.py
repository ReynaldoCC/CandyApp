# Generated by Django 2.2.2 on 2020-06-18 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_documento', '0006_auto_20200618_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpvdocumento',
            name='clasificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dpv_documento.TipoDPVDocumento', verbose_name='Clasificacion'),
        ),
    ]