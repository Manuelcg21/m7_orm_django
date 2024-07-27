from main.models import Curso, Estudiante, Profesor

def crear_curso(codigo, nombre, version):
    c = Curso(codigo=codigo, nombre=nombre, version=version)
    c.save()

def crear_profesor(rut, nombre, apellido):
    p = Profesor(rut=rut, nombre=nombre, apellido=apellido)
    p.save()

def crear_estudiante(rut,nombre,apellido,fecha_nac):
    e = Estudiante(rut=rut, nombre=nombre, apellido=apellido, fecha_nac=fecha_nac, activo=True)
    e.save()

def crear_direccion():
    pass

def obtiene_estudiante():
    pass

def obtiene_profesor():
    pass

def obtiene_curso():
    pass

def agrega_profesor_a_curso(profesor_rut, curso_codigo):
    # 1. Me traigo ambas entidades
    p = Profesor.objects.get(rut=profesor_rut)
    c = Curso.objects.get(codigo=curso_codigo)
    # 2. Vinculo las variables
    c.profesor = p
    c.save()
    
def agrega_cursos_a_estudiantes(curso_codigo, estudiante_rut):
    # 1. recuperamos el curso y el estudiante que deseamos vincular
    c = Curso.objects.get(codigo=curso_codigo)
    e = Estudiante.objects.get(rut=estudiante_rut)
    # 2. Vinculamos ambas entidades
    c.estudiantes.add(e)


def imprime_estudiante_cursos():
    pass

