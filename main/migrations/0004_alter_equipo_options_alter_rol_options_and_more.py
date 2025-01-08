# Generated by Django 5.1.2 on 2025-01-07 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_jugador_rol_jugador_roles'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipo',
            options={'verbose_name_plural': 'Equipos'},
        ),
        migrations.AlterModelOptions(
            name='rol',
            options={'verbose_name_plural': 'Roles'},
        ),
        migrations.AddField(
            model_name='equipo',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='jugador',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]
