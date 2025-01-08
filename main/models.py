# encoding: utf-8

from django.db import models


class Region(models.Model):
    idRegion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Región")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre', )
        verbose_name_plural = "Regiones"


class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Rol")

    def __str__(self):
        return self.nombre

    class Meta:
        # ordering = ('nombre', )
        verbose_name_plural = "Roles"


class Equipo(models.Model):
    idEquipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Equipo")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Región")
    capitan = models.CharField(max_length=50, verbose_name="Capitán", null=True, blank=True)
    entrenador = models.CharField(max_length=50, verbose_name="Entrenador", null=True, blank=True)
    ganancias = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ganancias Totales", default=0.0)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Equipos"


class Jugador(models.Model):
    idJugador = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=50, unique=True, verbose_name="Nick del Jugador")
    nombre_real = models.CharField(max_length=100, verbose_name="Nombre Real", null=True, blank=True)
    nacionalidad = models.CharField(max_length=50, verbose_name="Nacionalidad", null=True, blank=True)
    roles = models.ManyToManyField(Rol, related_name="jugadores", verbose_name="Roles del Jugador")
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Equipo Actual")
    ganancias = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ganancias Totales", default=0.0)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)

    def __str__(self):
        return self.nick

    class Meta:
        ordering = ('nick', )
        verbose_name_plural = "Jugadores"