# Generated by Django 2.2.2 on 2020-03-20 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpv_quejas', '0010_auto_20200207_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignaquejadpto',
            name='rechazada',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asignaquejatecnico',
            name='rechazada',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
