from django.core.management.base import BaseCommand, CommandParser
from main.services import obtener_inmuebles_region

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-f', '--f', type=str, nargs='+',)

    def handle(self, *args, **kwargs):
        filtro = None
        if 'f' in kwargs.keys() and kwargs['f'] is not None:
            filtro = kwargs['f'][0]
        inmuebles = obtener_inmuebles_region(filtro)

        with open('data/inmuebles_regiones.txt', 'w') as file:
            for inmueble in inmuebles:
                linea = str(inmueble)
                print(inmueble)