from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Alumno(models.Model):
    
    def validar_nombre_completo(value):
        partes = value.strip().split()

        if len(partes) < 2:
            raise ValidationError("Debe ingresar nombre y apellido.")
        
    nombre = models.CharField(max_length=100, unique=True, validators=[validar_nombre_completo])
    edad = models.IntegerField(validators=[MinValueValidator(3)])
    curso = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre