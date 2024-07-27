from django.shortcuts import render, HttpResponse
from main.services import crear_curso, crear_estudiante, agrega_cursos_a_estudiantes

# Create your views here.
def test(req):
    agrega_cursos_a_estudiantes