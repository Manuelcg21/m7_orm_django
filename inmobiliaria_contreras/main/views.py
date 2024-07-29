from django.shortcuts import render, redirect
from main.forms import RegisterForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.services import editar_user_sin_password, change_pass, crear_user
from main.models import Comuna, Region, Inmueble, UserProfile
from django.db.models import Q

# Create your views here.
@login_required
def indexView(req):
    datos= req.GET
    region_cod = datos.get('region_cod', '')
    comuna_cod = datos.get('comuna_cod', '')
    palabra = datos.get('palabra', '')
    user = req.user
    inmuebles = filtrar_inmuebles(region_cod, comuna_cod, palabra)
    comunas= Comuna.objects.all()
    regiones = Region.objects.all()
    context = {
        'comunas': comunas,
        'regiones': regiones,
        'inmuebles': inmuebles
    }
    return render(req, 'home.html', context)

def filtrar_inmuebles(region_cod, comuna_cod, palabra):
    filtro_palabra = None
    if palabra != '':
        filtro_palabra = Q(nombre__icontains=palabra) | Q (descripcion__icontains=palabra) | Q (comuna__nombre__icontains=palabra)
        
    filtro_ubicacion = None
    #Caso 1: comuna_cod != ''
    if comuna_cod != '':
        comuna = Comuna.objects.get(cod=comuna_cod)
        filtro_ubicacion = Q(comuna=comuna)
    elif region_cod != '':
        region = Region.objects.get(cod=region_cod)
        comunas_region = region.comunas.all()
        filtro_ubicacion = Q(comuna__in=comunas_region)
        
    if filtro_ubicacion is None and filtro_palabra is None:
        return Inmueble.objects.all()
    elif filtro_ubicacion is not None and filtro_palabra is None:
        return Inmueble.objects.filter(filtro_ubicacion)
    elif filtro_ubicacion is None and filtro_palabra is not None:
        return Inmueble.objects.filter(filtro_palabra)
    elif filtro_ubicacion is not None and filtro_palabra is not None:
        return Inmueble.objects.filter(filtro_palabra & filtro_ubicacion)
    return []
    
    #  #Caso 2: comuna_cod == '' and region_cod != ''
    
    # elif comuna_cod == '' and region_cod != '':
    #     region = Region.objects.get(cod=region_cod)
    #     comunas = Comuna.objects.filter(region=region)
    #     return Inmueble.objects.filter(comuna__in=comunas)
    # #Caso 3: comuna_cod == '' and region_cod == ''
    # else:
    
    
    #     inmuebles = Inmueble.objects.all()
    #     return inmuebles

@login_required
def profile(req):
    user = req.user
    mis_inmuebles= None
    if user.user_profile.rol == 'arrendador':
        mis_inmuebles= user.inmuebles.all()
    elif user.user_profile.rol == 'arrendatario':
        pass
    
    context = {
        'mis_inmuebles': mis_inmuebles
    }
        
    return render(req, 'profile.html', context)

@login_required
def edit_user(req):
    print(req.POST)
    #1. Obtengo el usuario actual
    current_user = req.user
    #2. Modifico los atributos del user
    if req.POST['telefono'].strip() != '':
        editar_user_sin_password(
            current_user.username,
            req.POST['first_name'],
            req.POST['last_name'],
            req.POST['email'],
            req.POST['direccion'],
            req.POST['rol'],
            req.POST['telefono']
        )
    else:
        editar_user_sin_password(
            current_user.username,
            req.POST['first_name'],
            req.POST['last_name'],
            req.POST['email'],
            req.POST['direccion'],
            req.POST['rol'])   
    messages.success(req, '¡Ha actualizado sus datos con éxito!')
    return redirect('/')

def change_password(req):
    #1. Recibo los datos del formulario
    password = req.POST['password']
    pass_repeat = req.POST['pass_repeat']
    change_pass(req, password, pass_repeat)
    return redirect('/accounts/profile')
    
def register(req):
    if req.method == 'GET':
        return render(req, 'registration/register.html')
    #en caso de POST
    username = req.POST['username'] 
    email = req.POST['email'] 
    password = req.POST['password']
    first_name = req.POST['first_name']
    last_name = req.POST['last_name']
    direccion = req.POST['direccion']
    telefono = req.POST['telefono']
    rol = req.POST['rol']
    pass_confirm = req.POST['pass_confirm']
    user = crear_user(
        username, first_name, last_name, email, password, pass_confirm, direccion, rol, telefono
        )
    messages.success(req, '¡El usuario ha sido creado con éxito!')
    return redirect('/')