from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator




# Create your models here.

class User(AbstractUser):
    pass

class Cliente (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default='2')
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length =50, blank =True)
    apellido_materno = models.CharField(max_length= 50, blank = True)
    nacimiento = models.DateField(blank=True, null=True)
    calle = models.CharField(max_length= 100, blank=True)
    numero = models.CharField(max_length= 10, blank=True )
    colonia = models.CharField(max_length = 100, blank=True)
    ciudad = models.CharField(max_length = 100, blank=True)
    cp = models.CharField(max_length=5, blank=True)
    telefono_regex = RegexValidator(regex=r'^\d{10,10}$', message="Formato permitido: '4431234567'. Diez digitos.")
    telefono = models.CharField(blank = True, validators=[telefono_regex], max_length=13)
    email = models.EmailField(max_length=250, blank= True, default=None) 

    # def __str__(self):
    #     string = self.nombre + " " + self.apellido_paterno + " " + self.apellido_materno
    #     return string 
    
class Pedidos(models.Model):
    cliente_id = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cantidad_inicial = models.DecimalField(max_digits= 7, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits = 7, decimal_places=2, default=0)
    #parcialidades = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(48)])
    #interes = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    por_entregar = models.BooleanField(default = False)
    entregado = models.BooleanField(default=False)

class Articulos(models.Model):
    pedido_id = models.ForeignKey(Pedidos, on_delete=models.PROTECT, related_name="articulos_encargados")
    url = models.URLField(blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits = 6, decimal_places=2)

    
class Abonos(models.Model):
    pedido_id = models.ForeignKey(Pedidos, on_delete= models.CASCADE, default=None)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)