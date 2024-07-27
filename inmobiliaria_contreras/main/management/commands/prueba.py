from typing import Any
from django.core.management.base import BaseCommand
from main.services import * 

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        #crear_user('1234567-8', 'Manuel', 'Contreras', 'mmanuel@gmail.com', '12345', '12345', 'Bellavista 914')
        #editar_user('1234567-8', 'Manuel', 'Contreras', 'mmanuelcontreras@gmail.com', '12345', 'Avenida Quilpue 914')
        crear_inmueble('Bella casa de piedra', 'Amoblada con dinosaurios', 120, 250, 1, 3, 1, 'Av. Rocosa 331', 'casa', 500_000, '05606', '1234567-8')
