# Generated by Django 2.2 on 2020-01-19 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_nomencladores', '0007_auto_20200119_0452'),
        ('dpv_persona', '0002_auto_20200117_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='personajuridica',
            name='cpopular',
            field=models.ForeignKey(blank=True, default='', help_text='Consejo popular donde recide la persona', on_delete=django.db.models.deletion.CASCADE, to='dpv_nomencladores.ConsejoPopular', verbose_name='Consejo Popular'),
        ),
        migrations.AddField(
            model_name='personanatural',
            name='cpopular',
            field=models.ForeignKey(blank=True, default='', help_text='Consejo popular donde recide la persona', on_delete=django.db.models.deletion.CASCADE, to='dpv_nomencladores.ConsejoPopular', verbose_name='Consejo Popular'),
        ),
    ]