from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(AbstractUser):
    pass

class Cliente (models.Model):

    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length =50, blank =True)
    apellido_materno = models.CharField(max_length= 50, blank = True)
    nacimiento = models.DateField()
    calle = models.CharField(max_length= 100)
    numero = models.CharField(max_length= 10)
    colonia = models.CharField(max_length = 100)
    ciudad = models.CharField(max_length = 100)
    cp = models.CharField(max_length=4)

class Prestamo(models.Model):
    cliente_id = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cantidad_inicial = models.DecimalField(max_digits= 5, decimal_places=2)
    balance = models.DecimalField(max_digits = 5, decimal_places=2)
    parcialidades = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(48)])
    fecha = models.DateTimeField(auto_now_add=True)