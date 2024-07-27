from typing import Any
from main.models import Estudiante, Curso, Direccion, Profesor
from main.services import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        p = crear_profesor('11.219.854-7', 'Profesor', 'Heimerdinger')
        c = crear_curso('KL01', 'Introduccion a Python', 1)
        a = crear_estudiante('18.970.587-5', 'Akshan', 'Shurima', '2001-01-01')