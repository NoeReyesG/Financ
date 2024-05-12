from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django  import forms
from .models import Cliente, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



#Formulario para registrar un nuevo cliente
class customerForm(forms.Form):
    
    nombre = forms.CharField(label = "Nombre", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    apellido_paterno = forms.CharField(label = "Apellido Paterno", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    apellido_materno = forms.CharField(label = "Apellido Materno", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    nacimiento = forms.DateField(label = "Fecha de Nacimiento", widget = forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    calle = forms.CharField(label="Calle", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    numero = forms.CharField(label="Número", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    colonia = forms.CharField(label="Colonia", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    ciudad = forms.CharField(label="Ciudad", max_length=50, widget = forms.TextInput(attrs = {'class':'form-control'}))
    cp = forms.CharField(label = "C.P.", max_length=4, widget = forms.TextInput(attrs = {'class':'form-control'}))

@login_required
def index(request):
    return render(request, "financiera/index.html")


def login_user(request):
    '''Inicio de sesión del usuario'''
    if request.method == 'POST':
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "financiera/login.html", {
                "message": "Usuario o password incorrecto"
            })
    else:
        return render(request, "financiera/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def signin(request):
    '''Registro de un nuevo usuario que utilizara la aplicación.'''
    if request.method == 'POST':
        pass
        username = request.POST["username"]
        email = request.POST["email"]
        nombre = request.POST["first-name"]
        apellido = request.POST["last-name"]

        # Asegurar que la confirmación coincida
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "financiera/register.html", {
                "message": "Confirmación de password no coincide"
            })
        # Intento de crear un nuevo usuario
        try:
            usuario = User.objects.create_user(username, email, password, first_name = nombre, last_name = apellido)
            usuario.save()
        except IntegrityError:
            return render(request, 'financiera/register.html', {
                'message': 'El usuario ya existe'
            })
        login(request, usuario)
        return HttpResponseRedirect(reverse("home"))


    else:
        return render(request, "financiera/register.html")

@login_required
def registrarCliente(request):
    '''Registra un nuevo cliente que adquirirá los servicios'''
    context = {}
    
    if request.method == 'POST':
        
        cliente =  customerForm(request.POST)
        if cliente.is_valid():
            cliente = cliente.cleaned_data
        
            try:
                Cliente.objects.get(nombre=cliente["nombre"], apellido_materno = cliente["apellido_materno"], nacimiento=cliente["nacimiento"])
            except:
                print(cliente)
                clienteDB=Cliente(**cliente)
                print(clienteDB)
                clienteDB.save()
                context["registerclientform"] = customerForm()
                context["mensaje_exito"] = "Cliente registrado correctamente"
                return render(request, "financiera/registrarCliente.html", context)
            else:
                context["registerclientform"] = customerForm()
                context["mensaje_error"] = "Cliente resgistrado previamente "
                return render(request, "financiera/registrarCliente.html", context)

            # try:
            #     clienteDB = Cliente.objects.filter()
            #     user = Cliente.objects.create_user(clienteDB)
            #     user.save()
            # except IntegrityError:
            #     return render(request, "financiera/registarCliente.html", {
            #             "message": "Username already taken."
            #     })
        print("entró a post")

        return HttpResponse("Ok")
    else:
        context['registerclientform'] = customerForm()
        return render(request, 'financiera/registrarCliente.html', context)
    

def consultar_cliente(request):
    if request.method == 'POST':
        filtro = {}

        if request.POST['first_name']:
            filtro['nombre'] = request.POST['first_name']
        if request.POST['last_name1']:
            filtro['apellido_paterno'] = request.POST['last_name1']
        if request.POST['last_name2']:
            filtro['apellido_materno'] = request.POST['last_name2'] 
        if request.POST['nacimiento']:
            filtro['nacimiento'] = request.POST['nacimiento']

        #print(filtro)
        clientes = Cliente.objects.filter(**filtro)
        print(clientes)
        for cliente in clientes:
            print(cliente.nacimiento)
            print(cliente.apellido_materno)
        print("algo")
        return render(request, "financiera/consultas.html", {
            "clientes" : clientes
        })
    else:
        return render(request, "financiera/consultas.html")