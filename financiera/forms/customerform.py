from django import forms
from django.core.validators import RegexValidator

#Formulario para registrar un nuevo cliente
class customerForm(forms.Form):
    
    nombre = forms.CharField(label = "Nombre", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    apellido_paterno = forms.CharField(label = "Apellido Paterno", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    apellido_materno = forms.CharField(required = False, label = "Apellido Materno", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    nacimiento = forms.DateField(label = "Fecha de Nacimiento", widget = forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    calle = forms.CharField(label="Calle", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    numero = forms.CharField(label="Número", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    colonia = forms.CharField(label="Colonia", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    ciudad = forms.CharField(label="Ciudad", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    cp = forms.CharField(label = "C.P.", max_length=4, widget = forms.TextInput(attrs = {'class':'form-control'}))
    telefono_regex = RegexValidator(regex=r'\d{10,10}$', message="Formato permitido: '+52 4431234567'. Diez digitos.")
    telefono = forms.CharField(validators=[telefono_regex], max_length=13, required=False, widget = forms.TextInput(attrs = {'class':'form-control', 'type':'number'})) 
    email = forms.EmailField(required = False, widget = forms.TextInput(attrs = {'class':'form-control'}))