# Generated by Django 2.2 on 2020-01-18 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_quejas', '0003_auto_20200117_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignaquejadpto',
            name='rechazada',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='asignaquejatecnico',
            name='rechazada',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.CreateModel(
            name='QuejaNotificada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Eliminado')),
                ('notificada', models.DateTimeField(default=None, null=True, verbose_name='Notificada')),
                ('queja', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificada', to='dpv_quejas.Queja')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]