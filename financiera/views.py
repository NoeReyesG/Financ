from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django  import forms
from .models import Cliente, User, Pedidos, Abonos
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.validators import RegexValidator
from django.core.serializers import serialize
from decimal import Decimal



#Formulario para registrar un nuevo cliente
class customerForm(forms.Form):
    
    nombre = forms.CharField(label = "Nombre", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    apellido_paterno = forms.CharField(label = "Apellido Paterno", required=False, max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    apellido_materno = forms.CharField(required = False, label = "Apellido Materno", max_length = 100, widget= forms.TextInput(attrs = {'class':'form-control'}))
    nacimiento = forms.DateField(label = "Fecha de Nacimiento", required=False, widget = forms.DateInput(attrs={'type': 'date', 'class':'form-control'}))
    calle = forms.CharField(label="Calle", max_length=50, required=False, widget = forms.TextInput(attrs = {'class':'form-control'}))
    numero = forms.CharField(label="Número", max_length=50, required=False, widget = forms.TextInput(attrs = {'class':'form-control'}))
    colonia = forms.CharField(label="Colonia", max_length=50, required=False, widget = forms.TextInput(attrs = {'class':'form-control'}))
    ciudad = forms.CharField(label="Ciudad", max_length=50, required=False, widget = forms.TextInput(attrs = {'class':'form-control'}))
    cp = forms.CharField(label = "C.P.", max_length=5, required=False, widget = forms.TextInput(attrs = {'class':'form-control'}))
    telefono_regex = RegexValidator(regex=r'\d{10,10}$', message="Formato permitido: '+52 4431234567'. Diez digitos.")
    telefono = forms.CharField(validators=[telefono_regex], max_length=13, required=False, widget = forms.TextInput(attrs = {'class':'form-control', 'type':'number'})) 
    email = forms.EmailField(max_length = 250, required = False, widget = forms.TextInput(attrs = {'class':'form-control', 'type':'email'}))


def index(request):
    if request.user.is_authenticated:
        return render(request, "financiera/index.html")
    else:
        return HttpResponseRedirect(reverse('login'))

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
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
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

    # resaltar navbar link 
    context["nuevoCliente"]="active"
    
    if request.method == 'POST':
        
        cliente =  customerForm(request.POST)
        if cliente.is_valid():
            cliente = cliente.cleaned_data

            try:
                Cliente.objects.get(user_id = request.user,
                                    nombre=cliente["nombre"], 
                                    apellido_materno = cliente["apellido_materno"], 
                                    nacimiento=cliente["nacimiento"])
            except:
                print(cliente)
                clienteDB=Cliente(user_id = request.user, **cliente)
                print(clienteDB)
                clienteDB.save()
                context["registerclientform"] = customerForm()
                context["mensaje_exito"] = "Cliente registrado correctamente"
                return render(request, "financiera/registrarCliente.html", context)
            else:
                context["registerclientform"] = customerForm()
                context["mensaje_error"] = "Cliente resgistrado previamente "
                return render(request, "financiera/registrarCliente.html", context)

        return HttpResponse("Invalid Data")
    else:
        context['registerclientform'] = customerForm()
        return render(request, 'financiera/registrarCliente.html', context)
    
@login_required
def consultar_cliente(request):
    if request.method == 'POST':
        filtro = {'user_id': request.user}

        if request.POST['first_name']:
            filtro['nombre__iexact'] = request.POST['first_name']
        if request.POST['last_name1']:
            filtro['apellido_paterno__iexact'] = request.POST['last_name1']
        if request.POST['last_name2']:
            filtro['apellido_materno__iexact'] = request.POST['last_name2'] 
        if request.POST['nacimiento']:
            filtro['nacimiento'] = request.POST['nacimiento']

        #print(filtro)
        clientes = Cliente.objects.filter(**filtro)
        print(clientes)
        for cliente in clientes:
            print(cliente.nacimiento)
            print(cliente.telefono)
        print("algo")
        return render(request, "financiera/consultas.html", {
            "clientes" : clientes,
            # resaltar navbar link
            "consultarCliente": "active"
        })
    else:
        return render(request, "financiera/consultas.html", {
            "consultarCliente" : "active"
        })
    

#Administración de cliente
@login_required
def cliente_config(request, id=None, mensaje=None):
    context = {}
    if request.method == 'POST':
        pass
    else:
        if id:
            cliente = Cliente.objects.filter(user_id = request.user, id = id)
            pedidos = Pedidos.objects.filter(cliente_id = cliente[0])
            context['cliente'] = cliente[0]
            context['pedidos'] = pedidos
            context['mensaje'] = mensaje
    return render(request, "financiera/cliente.html", context)


@login_required
def update_cliente(request, cliente_id):

    if request.method == 'POST':
        body = request.body
        print(body)
        return HttpResponse("preparing edit")



# def actualizar_cliente(cliente, pk):
@login_required
def nuevo_pedido(request, cliente_id):
    if request.method == 'POST':
        cliente = Cliente.objects.get(pk=cliente_id, user_id = request.user)
        nuevo_pedido = Pedidos(cliente_id = cliente)
        nuevo_pedido.save()
        return HttpResponseRedirect(reverse("cliente", kwargs={"id": cliente_id}))


@login_required
def agregar_articulo(request):
    #  if request.method == 'POST':
    #     cantidad = request.POST['cantidad']
    #     parcialidades = request.POST['parcialidades']
    #     interes = request.POST['interes']

    #     cliente = Cliente.objects.get(pk=cliente_id, user_id = request.user)
    pass


@login_required
def pago(request, pedido_id):
    # Registra un pago
    context = {}
    if request.method == 'POST':
        cantidad = request.POST['pagoInp'+str(pedido_id)]
        # user = User.objects.filter(id=request.user)
        pedido = Pedidos.objects.get(id = pedido_id)
         
        abono = Abonos(pedido_id = pedido, cantidad = cantidad)
        pedido.balance = pedido.balance - Decimal(cantidad)
        if pedido.balance >= 0:
            try:
                abono.save()
                pedido.save()
            except:
                 return redirect(reverse("cliente_mensaje", kwargs={'id':pedido.cliente_id.pk, 'mensaje':'fail'}))
        else: 
            context['mensaje'] = "un mensaje"
            return redirect("cliente", id=pedido.cliente_id.pk)
          
            #return HttpResponse("El pago es mayor a lo que se debe, favor de revisar")
        print(request.user, pedido_id, abono)
       
        return redirect(reverse("cliente_mensaje", kwargs={'id':pedido.cliente_id.pk, 'mensaje':'success'}))
        #return redirect (reverse("cliente_mensaje", context))

    
@login_required
def pedidos(request):
    pedidos = Pedidos.objects.all()
    pedidos = serialize("json", pedidos)
    print(pedidos)
    return JsonResponse(pedidos, safe=False)