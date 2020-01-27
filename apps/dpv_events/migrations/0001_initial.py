# Generated by Django 2.1 on 2019-04-10 22:34

import apps.dpv_events.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=apps.dpv_events.models.generate_code_acta, max_length=25)),
                ('body', models.TextField()),
                ('date_created', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'actas',
            },
        ),
        migrations.CreateModel(
            name='Acuerdo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=apps.dpv_events.models.generate_code_acuerdo, max_length=25)),
                ('asunto', models.CharField(max_length=255)),
                ('date_finish', models.DateTimeField()),
                ('is_done', models.BooleanField(default=False)),
                ('date_done', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'acuerdos',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_programed', models.DateTimeField()),
                ('site', models.CharField(max_length=255)),
                ('month', models.IntegerField()),
                ('is_extraordinario', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('date_done', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'eventos',
            },
        ),
        migrations.CreateModel(
            name='Frecuencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('days', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'frecuencias',
            },
        ),
        migrations.CreateModel(
            name='ResponsableAcuerdo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acuerdo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_events.Acuerdo')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'responsables',
            },
        ),
        migrations.CreateModel(
            name='RespuestaAcuerdo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField()),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_events.ResponsableAcuerdo')),
            ],
            options={
                'verbose_name_plural': 'respuestaacuerdos',
            },
        ),
        migrations.CreateModel(
            name='TemaEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=255)),
                ('es_sugerido', models.BooleanField(default=False)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_events.Evento')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'temas de evento',
            },
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('frecuencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dpv_events.Frecuencia')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Permission')),
            ],
            options={
                'verbose_name_plural': 'tipos de eventos',
            },
        ),
        migrations.AddField(
            model_name='evento',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_events.TipoEvento'),
        ),
        migrations.AddField(
            model_name='evento',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acuerdo',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpv_events.Evento'),
        ),
        migrations.AddField(
            model_name='acta',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dpv_events.Evento'),
        ),
    ]