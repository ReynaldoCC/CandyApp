# Generated by Django 2.2 on 2020-01-18 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dpv_quejas', '0004_auto_20200118_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='quejanotificada',
            name='notificador',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Quien notifica.'),
        ),
    ]
