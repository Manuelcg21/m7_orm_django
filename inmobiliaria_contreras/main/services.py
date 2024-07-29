from django.contrib.auth.models import User
from main.models import UserProfile, Inmueble, Comuna
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db import connection
from django.contrib import messages
from django.core.exceptions import ValidationError


def crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, tipo_inmueble, precio, comuna_cod, propietario_rut):
    
    comuna = Comuna.objects.get(cod=comuna_cod)
    propietario = User.objects.get(username=propietario_rut)

    Inmueble.objects.create(nombre=nombre, descripcion=descripcion, m2_construidos=m2_construidos, m2_totales=m2_totales, num_estacionamientos=num_estacionamientos, num_habitaciones=num_habitaciones, num_baños=num_baños, direccion=direccion, tipo_inmueble=tipo_inmueble, precio=precio, comuna=comuna, propietario=propietario)

def editar_inmueble(inmueble_id, nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, tipo_inmueble, precio, comuna, propietario_rut):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(nombre=comuna)
    inmueble.nombre = nombre
    inmueble.descripcion = descripcion 
    inmueble.m2_construidos = m2_construidos
    inmueble.m2_totales = m2_totales
    inmueble.num_estacionamientos = num_estacionamientos
    inmueble.num_habitaciones = num_habitaciones
    inmueble.num_baños = num_baños
    inmueble.direccion = direccion 
    inmueble.tipo_inmueble = tipo_inmueble
    inmueble.precio = precio
    inmueble.comuna = comuna
    inmueble.propietario = propietario_rut
    inmueble.save()

def eliminar_inmuebles(inmueble_id):
    
    inmueble = Inmueble.objects.get(id=inmueble_id)
    inmueble.delete()

def crear_user(username, first_name, last_name, email, password, pass_confirm, direccion, rol ,telefono= None)-> list[bool, str]:
    #1. Validamos si las password coinciden
    if password != pass_confirm:
        return False
    #2. creamos el objeto user
    try:
        user = User.objects.create_user(
        username, email, password,
        first_name=first_name,
        last_name=last_name,
    )
    except IntegrityError:
        #se le da feedback al usuario
        return False, 'RUT DUPLICADO'
        #3.  Creamos el UserProfile
    UserProfile.objects.create(
        direccion=direccion,
        telefono=telefono,
        user=user,
        rol = rol,
        )
    return True

def editar_user(rut, first_name, last_name, email, password, direccion, telefono= None)->list[bool, str]:   
    user = User.objects.get(username=rut)
    # Actualizar los campos del usuario utilizando update
    User.objects.filter(username=rut).update(
        first_name=first_name,
        last_name=last_name,
        email=email       
    )
    user.set_password(password)
    user.save()
    # Actualizar el perfil del usuario utilizando update
    UserProfile.objects.filter(user=user).update(
        direccion=direccion,
        telefono=telefono
    )
    return user

def editar_user_sin_password(rut, first_name, last_name, email, direccion, rol, telefono= None)->list[bool, str]:
    user = User.objects.get(username=rut)
    # Actualizar los campos del usuario utilizando update
    User.objects.filter(username=rut).update(
    first_name=first_name,
    last_name=last_name,
    email=email)
        # Actualizar el perfil del usuario utilizando update
    UserProfile.objects.filter(user=user).update(
        direccion=direccion,
        telefono=telefono,
        rol=rol
    )
    return user
    
def eliminar_user(user_id):
    User.objects.get(id=user_id).delete()

def obtener_inmuebles_comunas(filtro):
    if filtro is None:
        return Inmueble.objects.all().order_by('comuna')
    # si llegamos acá, significa que SI hay un filtro
    # select * from main_inmueble where nombre like '%Elegante%' or descripcion like '%Elegante%';
    return Inmueble.objects.filter(Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro)).order_by('comuna')

def obtener_inmuebles_regiones(filtro):
    consulta = 'select * from main_inmueble as I join main_comuna as C on I.comuna_id = C.cod join main_region as R on C.region_id = R.cod order by R.cod'
    if filtro is not None:
        consulta = f"select * from main_inmueble as I join main_comuna as C on I.comuna_id = C.cod join main_region as R on C.region_id = R.cod where I.nombre like'%{filtro}%' or I.descripcion like '%{filtro}%' order by R.cod"
        #return Inmueble.objects.raw(consulta)
        cursor =connection.cursor()
        cursor.execute(consulta)
        registros = cursor.fetchall()
        return registros
        #return Inmueble.objects.filter(nombre__icontains=filtro).order_by('comuna')

def change_pass(req, password, pass_repeat):
    #2. Valido que ambas contraseñas coincidan
    if password != pass_repeat:
        messages.error(req, 'Las contraseñas no coinciden')
        return
    else:
    #3. Actualizamos la contraseña
        req.user.set_password(password)
        req.user.save()
        #4. Le avisamos al usuario que el cambio fue exitoso
        messages.success(req, 'Contraseña actualizada')