from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from main.models import Inmueble, Region, Comuna
from main.services import crear_inmueble as crear_inmueble_service, eliminar_inmuebles as eliminar_inmueble_service, editar_inmueble as editar_inmueble_service
from inmuebles.forms import InmuebleForm
from django.contrib.auth.decorators import login_required

# vamos a crear un test que sólo pasan los 'arrendadores'
def solo_arrendadores(user):
  if user.user_profile.rol == 'arrendador' or user.is_staff == True:
    return True
  else:
    return False

@login_required
def nuevo_inmueble(req):
  # nos traemos la información de las comunas y las regiones
  regiones = Region.objects.all()
  comunas = Comuna.objects.all()
  # pasar los datos requeridos por el formulario
  context = {
    'tipos_inmueble': Inmueble.tipos,
    'regiones': regiones,
    'comunas': comunas
  }
  return render(req, 'nuevo_inmueble.html', context)

@user_passes_test(solo_arrendadores)
def crear_inmueble(req):
  # obtener el rut del usuario
  propietario_rut = req.user.username
  # validar metraje (construídos vs totales)
  crear_inmueble_service(
    req.POST['nombre'],
    req.POST['descripcion'],
    int(req.POST['m2_construidos']),
    int(req.POST['m2_totales']),
    int(req.POST['num_estacionamientos']),
    int(req.POST['num_habitaciones']),
    int(req.POST['num_baños']),
    req.POST['direccion'],
    req.POST['tipo_inmueble'],
    int(req.POST['precio']),
    req.POST['comuna_cod'],
    propietario_rut
  )
  messages.success(req, 'Propiedad Creada')
  return redirect('/')

def solo_arrendatario(user):
    if user.groups.filter(name='arrendatario').exists():
      return True
    return HttpResponse('Solo para arrendatarios')

@user_passes_test(solo_arrendadores)
def editar_inmueble(req, id):
  if req.method == 'GET':
    # 1. Obtengo elinmueble a editar
    inmueble = Inmueble.objects.get(id=id)
    # 2. Obtengo las regiones y comunas
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    # 2.5 Obtengo el código de la region
    cod_region = inmueble.comuna.region.cod
    # 3. Creo el 'context' con toda la info que requiere el template
    context = {
      'inmueble': inmueble,
      'regiones': regiones,
      'comunas': comunas,
      'cod_region': cod_region
    }
    return render(req, 'editar_inmueble.html', context)
  else:
    #req.method == 'POST'
        propietario_rut = req.user.username
        editar_inmueble_service(
            id,
            req.POST['nombre'],
            req.POST['descripcion'],
            int(req.POST['m2_construidos']),
            int(req.POST['m2_totales']),
            int(req.POST['cant_estacionamientos']),
            int(req.POST['cant_habitaciones']),
            int(req.POST['cant_baños']),
            req.POST['direccion'],
            int(req.POST['precio_mensual']),
            req.POST['tipo_inmueble'],
            req.POST['comuna_cod'],
            propietario_rut
            )
        messages.success(req, 'propiedad editada exitosamente')
        return redirect ('/')


@user_passes_test(solo_arrendadores)
def eliminar_inmueble(req, id):
  eliminar_inmueble_service(id)
  messages.error(req, 'Inmueble ha sido eliminado')
  return redirect('/accounts/profile/')

@login_required
def detalleInmueble(req, id):
    id=int(id)
    inmueble_encontrado = Inmueble.objects.get(id=id)
    
    context ={
        'inmueble_encontrado':inmueble_encontrado
    }
    return render(req, 'detalle.html', context)
