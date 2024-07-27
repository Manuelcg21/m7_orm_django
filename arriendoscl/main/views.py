from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
#from django.contrib.auth import user
from main.services import editar_user_sin_password, cambiar_password, crear_inmueble, editar_inmueble, eliminar_inmueble
from main.models import Comuna, Inmueble, Region
#from main.forms import InmuebleForm
# Create your views here.
@login_required
def home(req):
    datos = req.GET
    region_cod = datos.get('region_cod', '')
    comuna_cod = datos.get('comuna_cod', '')
    palabra = datos.get('palabra', '')
    #print(region_cod,cod_comuna,palabra)
    inmuebles = filtrar_inmuebles(region_cod,comuna_cod,palabra)
    comunas = Comuna.objects.all()
    regiones = Region.objects.all()
    context = {
        'inmuebles': inmuebles,
        'comunas': comunas,
        'regiones': regiones
    }
    return render(req, 'home.html', context)
# función para filtrar busqueda de inmuebles en página de inicio
def filtrar_inmuebles(region_cod,cod_comuna,palabra):
    #caso 1: cod_comuna != ''
    if cod_comuna != '':
        comuna = Comuna.objects.get(cod=cod_comuna)
        return Inmueble.objects.filter(comuna=comuna)
    #caso 2: cod_comuna == '' and region_cod != ''
    elif cod_comuna == '' and region_cod != '':
        region = Region.objects.get(cod=region_cod)
        comunas = Comuna.objects.filter(region=region)
        return Inmueble.objects.filter(comuna__in=comunas, nombre__icontains=palabra)
    #caso 3: cod_comuna == '' and region_cod == ''
    else:
        return Inmueble.objects.filter(nombre__icontains=palabra)
    # inmuebles = Inmueble.objects.all()
    # return inmuebles
    return Inmueble.objects.all()

@login_required
def profile(req):
    return render(req, 'profile.html')

@login_required
def edit_user(req):
    #obtener usuario actual
    current_user = req.user
    #modificar atributos del user
    if req.POST['telefono'].strip() != '':
        editar_user_sin_password(
            current_user.username,
            req.POST['first_name'],
            req.POST['last_name'],
            req.POST['email'],
            req.POST['direccion'],
            req.POST['rol'],
            req.POST['telefono'])
    else:
        editar_user_sin_password(
            current_user.username,
            req.POST['first_name'],
            req.POST['last_name'],
            req.POST['email'],
            req.POST['direccion'],
            req.POST['rol'])
    messages.success(req, "Se actualizaron tus datos!")
    return redirect('/')

def change_password(req):
    password =  req.POST['password']
    pass_repeat =  req.POST['pass_repeat']
    cambiar_password(req, password, pass_repeat)
    return redirect('/accounts/profile')
#pendientes para trabajar con grupos
def solo_arrendadores(user):
    if user.usuario.rol == 'arrendador' or user.is_staff == True:
        return True
    else:
        return False
# def solo_arrendatarios(req):
#     return HttpResponse('sólo arrendatarios')

@user_passes_test(solo_arrendadores)
def new_property(req):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    context = {
        'tipos_inmueble': Inmueble.tipo_inmueble,
        'regiones': regiones,
        'comunas': comunas
    }
    return render(req, 'new_property.html', context)

@user_passes_test(solo_arrendadores)
def create_property(req):
    #obtener rut usuario
    rut_propietario = req.user.username
    #se agrega propiedad a la base de datos
    crear_inmueble(
        req.POST['nombre'],
        req.POST['descripcion'],
        int(req.POST['m2_construidos']),
        int(req.POST['m2_totales']),
        int(req.POST['estacionamientos']),
        int(req.POST['habitaciones']),
        int(req.POST['num_baños']),
        req.POST['direccion'],
        req.POST['tipo_inmueble'],
        int(req.POST['precio']),
        req.POST['comuna_cod'],
        rut_propietario)
    #return HttpResponse('Propiedad agregada!')
    messages.success(req, "Su propiedad ha sido agregada!")
    return redirect('/')

@user_passes_test(solo_arrendadores)
def edit_property(req, id):
    if req.method == 'GET':
        #obtener inmueble a editar
        inmueble = Inmueble.objects.get(id=id)
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()
        cod_region = inmueble.comuna_id[0:2]
        #crear ModelForm
        #form = InmuebleForm(instance=inmueble)
        #variable usada para poblar el template con la info del inmueble
        context = {
            'inmueble': inmueble,
            'regiones': regiones,
            'comunas': comunas,
            'cod_region': cod_region
        }
        return render(req, 'edit_property.html', context)
    else:
        rut_propietario = req.user.username
        editar_inmueble(
            id,
            req.POST['nombre'],
            req.POST['descripcion'],
            int(req.POST['m2_construidos']),
            int(req.POST['m2_totales']),
            int(req.POST['estacionamientos']),
            int(req.POST['habitaciones']),
            int(req.POST['num_baños']),
            req.POST['direccion'],
            req.POST['tipo_inmueble'],
            int(req.POST['precio']),
            req.POST['comuna_cod'],
            rut_propietario)
        messages.success(req, "Cambios guardados con éxito!")
        return redirect('/')
        # return HttpResponse('es un POST')
    # rut_propietario = req.user.username
    # editar_inmueble(
    #     id,
    #     req.POST['nombre'],
    #     req.POST['descripcion'],
    #     int(req.POST['m2_construidos']),
    #     int(req.POST['m2_totales']),
    #     int(req.POST['estacionamientos']),
    #     int(req.POST['habitaciones']),
    #     int(req.POST['bagnos']),
    #     req.POST['direccion'],
    #     req.POST['tipo_inmueble'],
    #     int(req.POST['precio']),
    #     req.POST['comuna_cod'],
    #     rut_propietario)
    # messages.success(req, "Cambios guardados con éxito!")
    # return redirect('/')

@user_passes_test(solo_arrendadores)
def profile(req):
    user = req.user
    mis_inmuebles = None
    if user.usuario.rol == 'arrendador':
        mis_inmuebles = user.inmuebles.all()
    elif user.usuario.rol == 'arrendatario':
        pass
    context = {
        'mis_inmuebles': mis_inmuebles
    }
    # print(mis_inmuebles)
    return render(req, 'profile.html', context)

@user_passes_test(solo_arrendadores)
def delete_property(req,id):
    eliminar_inmueble(id)
    messages.error(req, 'Inmueble ha sido eliminado.')
    return redirect('/accounts/profile')