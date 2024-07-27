from typing import Any
from django.core.management.base import BaseCommand
from registro_conductores.services import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        crear_conductor('Pier', 'Na', '1970-03-03')
        #agregar_direccion('Av. Rocadura', '1234', 'Piedradura', 'v', 1)