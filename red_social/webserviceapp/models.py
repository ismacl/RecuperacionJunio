# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aficionados(models.Model):
    id_aficionado = models.IntegerField(db_column='Id_aficionado', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50)  # Field name made lowercase.
    gmail = models.CharField(db_column='Gmail', max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=10)  # Field name made lowercase.
    birthdate = models.DateField(db_column='birthDate')  # Field name made lowercase.
    registerdate = models.DateField(db_column='RegisterDate')  # Field name made lowercase.
    url_avatar = models.CharField(max_length=255, blank=True, null=True)
    token_sesion = models.BigIntegerField(db_column='Token_Sesion', blank=True, null=True)  # Field name made lowercase.
    id_equipo = models.IntegerField(db_column='Id_Equipo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aficionados'


class Comentarios(models.Model):
    id_comentarios = models.IntegerField(db_column='id_Comentarios', primary_key=True)  # Field name made lowercase.
    id_contenido = models.ForeignKey('Contenido', models.DO_NOTHING, db_column='Id_Contenido')  # Field name made lowercase.
    id_aficionado = models.ForeignKey(Aficionados, models.DO_NOTHING, db_column='Id_aficionado')  # Field name made lowercase.
    comentario = models.CharField(db_column='Comentario', max_length=50)  # Field name made lowercase.
    fecha_comentario = models.DateField(db_column='Fecha_comentario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comentarios'


class Contenido(models.Model):
    id_contenido = models.IntegerField(db_column='Id_Contenido', primary_key=True)  # Field name made lowercase.
    id_aficionado = models.ForeignKey(Aficionados, models.DO_NOTHING, db_column='Id_aficionado')  # Field name made lowercase.
    id_equipo = models.ForeignKey('Equipos', models.DO_NOTHING, db_column='Id_Equipo')  # Field name made lowercase.
    tipo_contenido = models.CharField(db_column='Tipo_Contenido', max_length=50)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    fecha_publicacion = models.DateField(db_column='Fecha_Publicacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contenido'


class Equipos(models.Model):
    id_equipo = models.IntegerField(db_column='Id_Equipo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    liga = models.CharField(db_column='Liga', max_length=50)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50)  # Field name made lowercase.
    año_fundacion = models.TextField(db_column='Año_Fundacion')  # Field name made lowercase. This field type is a guess.
    estadio = models.CharField(db_column='Estadio', max_length=50)  # Field name made lowercase.
    url_equipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipos'
