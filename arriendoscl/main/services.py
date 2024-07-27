from django.contrib.auth.models import User
from main.models import Comuna, UserProfile, Inmueble, Region
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db import connection
from django.contrib import messages

def crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, num_estacionamiento, num_habitaciones,num_baños, direccion, tipo_inmueble, precio, comuna_cod, propietario_rut):
    comuna = Comuna.objects.get(cod=comuna_cod)
    propietario = User.objects.get(username=propietario_rut)
    inmueble= Inmueble.objects.create(
        nombre=nombre, 
        descripcion=descripcion, 
        m2_construidos=m2_construidos, 
        m2_totales=m2_totales, 
        num_estacionamiento=num_estacionamiento, 
        num_habitaciones=num_habitaciones, 
        num_baños=num_baños, 
        direccion=direccion, 
        tipo_inmueble=tipo_inmueble, 
        precio=precio, 
        comuna=comuna, 
        propietario=propietario
        )
    inmueble.save()

def editar_inmueble(inmueble_id, nombre, descripcion, m2_construidos, m2_totales, num_estacionamiento, num_habitaciones, num_baños, direccion, tipo_inmueble, precio, comuna_cod, propietario_rut):
    inmueble = Inmueble.objects.get(id = inmueble_id)
    comuna = Comuna.objects.get(cod=comuna_cod)
    propietario = User.objects.get(username=propietario_rut)
    inmueble.nombre = nombre
    inmueble.descripcion = descripcion
    inmueble.m2_construidos = m2_construidos
    inmueble.m2_totales = m2_totales
    inmueble.num_estacionamientos = num_estacionamiento
    inmueble.num_habitaciones = num_habitaciones
    inmueble.num_baños = num_baños
    inmueble.direccion = direccion
    inmueble.tipo_inmueble = tipo_inmueble
    inmueble.precio = precio
    inmueble.comuna = comuna
    inmueble.propietario = propietario
    inmueble.save()

def eliminar_inmueble(inmueble_id):
    inmueble = Inmueble.objects.get(id = inmueble_id)
    inmueble.delete()

def crear_user(username, first_name, last_name, email, password, pass_confirm, direccion, telefono=None) -> list [bool, str]:
    # 1. Validamos que las password coincidan 
    if password != pass_confirm:
        return False, 'Las contraseñas no coinciden'
    # 2. Creamo el objeto user
    try:
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    except IntegrityError:
        # se le da feedback al usuario
        return False, 'RUT duplicado'
    # 3. Creamos el UserProfile
    UserProfile.objects.create(user=user, direccion=direccion, telefono=telefono)
    # 4. Si todo sale bien, retornamos True
    return True, None

def editar_user(username, first_name, last_name, email, password, direccion, telefono=None) ->list[bool, str]:
    # 1. Nos traemos el 'user' y modificamos sus datos
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(password)
    user.save()
    # 2. Nos traemos el 'user_profile' y modificamos sus datos
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono = telefono
    user_profile.save()

def eliminar_user(user_id):
    usuario = User.objects.get(username=user_id)
    usuario.delete()

def obtener_inmuebles_comuna(filtro):
    if filtro is None:
        return Inmueble.objects.all().order_by('comuna')
    # select * from main_inmueble where nombre like '%Elegante%' or descripcion like '%Elegante%'
    return Inmueble.objects.filter(Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro)).order_by('comuna')
def obtener_inmuebles_region(filtro):
    # if filtro is None:
    #     consulta = "select * from main_inmueble as I join main_comuna as C on I.comuna_id = C.cod join main_region as R on C.region_id = R.cod order by R.cod"
    #     return Inmueble.objects.raw(consulta)
    # return Inmueble.objects.filter(nombre__icontains=filtro).order_by('comuna')
    consulta = '''select I.nombre, I.descripcion, R.nombre as region from main_inmueble as I join main_comuna as C on I.comuna_id = C.cod join main_region as R on C.region_id = R.cod order by R.cod'''
    if filtro is not None:
        filtro = filtro.lower()
        consulta = f'''select I.nombre, I.descripcion, R.nombre as region from main_inmueble as I join main_comuna as C on I.comuna_id = C.cod join main_region as R on C.region_id = R.cod where I.nombre like '%{filtro}%' or I.descripcion like '%{filtro}%' order by R.cod'''
    cursor=connection.cursor()
    cursor.execute(consulta)
    registros = cursor.fetchall()
    return registros
def editar_user_sin_password(username, first_name, last_name, email, direccion, rol, telefono=None):
    # 1. Nos traemos el 'user' y modificamos sus datos
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    # 2. Nos traemos el 'user_profile' y modificamos sus datos
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono = telefono
    user_profile.rol = rol
    user_profile.save()
def cambiar_password(req, password, pass_repeat):
    if password != pass_repeat:
        messages.error(req, 'Las contraseñas no coinciden.')
        return
    req.user.set_password(password)
    req.user.save()
    messages.success(req, 'Contraseña actualizada.')