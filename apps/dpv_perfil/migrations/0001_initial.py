# Generated by Django 2.1 on 2019-04-10 22:32

import apps.dpv_perfil.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dpv_nomencladores', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dpv_persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notificacion_email', models.BooleanField(default=True, help_text='Marque para recibir las notificaciones por correo electrónico', verbose_name='Notificar por Email')),
                ('documentacion_email', models.BooleanField(default=True, help_text='Marque para recibir la documentación por correo electronico', verbose_name='Recibir Documentos por Email')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=apps.dpv_perfil.models.scramble_upload_avatar, verbose_name='avatars')),
                ('centro_trabajo', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='perfil_trabajo', to='dpv_nomencladores.CentroTrabajo', verbose_name='Unidad')),
                ('datos_personales', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_datos', to='dpv_persona.PersonaNatural', verbose_name='Datos Personales')),
                ('datos_usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_usuario', to=settings.AUTH_USER_MODEL, verbose_name='Datos del usuario')),
                ('depto_trabajo', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='perfil_area', to='dpv_nomencladores.AreaTrabajo', verbose_name='Departamento')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
    ]