# Generated by Django 2.2.2 on 2020-08-25 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_nomencladores', '0030_email_nombre_contacto'),
    ]

    operations = [
        migrations.AddField(
            model_name='telefono',
            name='nombre_contacto',
            field=models.CharField(blank=True, default='', help_text='Nombre de la persona que contacto por teléfono', max_length=220, verbose_name='Nombre de contacto'),
        ),
    ]
