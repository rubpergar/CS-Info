# Generated by Django 5.1.2 on 2025-01-05 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('idEquipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre del Equipo')),
                ('capitan', models.CharField(blank=True, max_length=50, null=True, verbose_name='Capitán')),
                ('entrenador', models.CharField(blank=True, max_length=50, null=True, verbose_name='Entrenador')),
                ('ganancias', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Ganancias Totales')),
            ],
            options={
                'verbose_name_plural': 'Equipos',
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('idRegion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Región')),
            ],
            options={
                'verbose_name_plural': 'Regiones',
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('idRol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Rol')),
            ],
            options={
                'verbose_name_plural': 'Roles',
                'ordering': ('nombre',),
            },
        ),
        migrations.RemoveField(
            model_name='denominacion',
            name='pais',
        ),
        migrations.RemoveField(
            model_name='vino',
            name='denominacion',
        ),
        migrations.RemoveField(
            model_name='vino',
            name='uvas',
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('idJugador', models.AutoField(primary_key=True, serialize=False)),
                ('nick', models.CharField(max_length=50, unique=True, verbose_name='Nick del Jugador')),
                ('nombre_real', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre Real')),
                ('nacionalidad', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nacionalidad')),
                ('ganancias', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Ganancias Totales')),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.equipo', verbose_name='Equipo Actual')),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.rol', verbose_name='Rol del Jugador')),
            ],
            options={
                'verbose_name_plural': 'Jugadores',
                'ordering': ('nick',),
            },
        ),
        migrations.AddField(
            model_name='equipo',
            name='jugadores',
            field=models.ManyToManyField(related_name='equipos', to='main.jugador', verbose_name='Jugadores'),
        ),
        migrations.AddField(
            model_name='equipo',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.region', verbose_name='Región'),
        ),
        migrations.DeleteModel(
            name='Pais',
        ),
        migrations.DeleteModel(
            name='Denominacion',
        ),
        migrations.DeleteModel(
            name='Uva',
        ),
        migrations.DeleteModel(
            name='Vino',
        ),
    ]
