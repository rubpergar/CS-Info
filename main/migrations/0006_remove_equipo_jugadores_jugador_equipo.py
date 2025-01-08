# Generated by Django 5.1.2 on 2025-01-07 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_jugador_equipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipo',
            name='jugadores',
        ),
        migrations.AddField(
            model_name='jugador',
            name='equipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.equipo', verbose_name='Equipo Actual'),
        ),
    ]