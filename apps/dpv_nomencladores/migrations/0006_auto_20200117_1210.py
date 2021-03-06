# Generated by Django 2.2 on 2020-01-17 12:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_nomencladores', '0005_auto_20200111_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='areatrabajo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='areatrabajo',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='areatrabajo',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='calle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='calle',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='calle',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='centrotrabajo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='centrotrabajo',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='centrotrabajo',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='clasificacionrespuesta',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clasificacionrespuesta',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='clasificacionrespuesta',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='codificadorasunto',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codificadorasunto',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='codificadorasunto',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='concepto',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='concepto',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='concepto',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='consejopopular',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consejopopular',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='consejopopular',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='destino',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='destino',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='destino',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='estado',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estado',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='estado',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='genero',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genero',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='genero',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='municipio',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='organismo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organismo',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='organismo',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='piso',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='piso',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='piso',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='procedencia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='procedencia',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='procedencia',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='provincia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provincia',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='provincia',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='tipoprocedencia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tipoprocedencia',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='tipoprocedencia',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AddField(
            model_name='tipoqueja',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tipoqueja',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='tipoqueja',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
    ]
