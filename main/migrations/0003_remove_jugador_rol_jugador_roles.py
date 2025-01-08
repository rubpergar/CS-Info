# Generated by Django 5.1.2 on 2025-01-05 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_equipo_region_rol_remove_denominacion_pais_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugador',
            name='rol',
        ),
        migrations.AddField(
            model_name='jugador',
            name='roles',
            field=models.ManyToManyField(related_name='jugadores', to='main.rol', verbose_name='Roles del Jugador'),
        ),
    ]
