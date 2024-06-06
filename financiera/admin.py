from django.contrib import admin
from .models import Cliente, User, Pedidos, Abonos

# Register your models here.
admin.site.register(Cliente)
admin.site.register(User)
admin.site.register(Pedidos)
admin.site.register(Abonos)