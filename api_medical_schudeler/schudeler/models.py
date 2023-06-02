from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_identificacion = models.CharField(max_length=50)
    celular = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'

class Citas(models.Model):
    sede = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    descripcion = models.TextField()
    activa = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.id
