from django.db import models

# Create your models here.
class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

class Curso(models.Model):
    cod = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=False)

    estudiantes = models.ManyToManyField(Estudiante, related_name='cursos')