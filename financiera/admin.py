from django.contrib import admin
from .models import Cliente, User, Prestamo, Abono

# Register your models here.
admin.site.register(Cliente)
admin.site.register(User)
admin.site.register(Prestamo)
admin.site.register(Abono)