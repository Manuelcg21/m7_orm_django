from registro_conductores.models import Conductor, Direccion, Vehiculo

def crear_conductor(nombre, apellido, fecha_nacimiento):
    c=Conductor(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento)
    c.save()

def agregar_direccion(calle, numero, comuna, region, conductor_id):
    d = Direccion(calle=calle, numero=numero, comuna=comuna, region=region, conductor_id=conductor_id)
    d.save()
    imprimir_modelos()

def imprimir_modelos():
    conductores = Conductor.objects.all()
    direcciones = Direccion.objects.all()
    print(conductores)
    print(direcciones)