from django.contrib import admin
from django.urls import path, include
from main.views import home, solo_arrendadores, solo_arrendatarios, profile, edit_user, change_password
#from inmuebles.views import nuevo_inmueble, crear_inmueble, editar_inmueble, eliminar_inmueble

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('accounts/profile/', profile, name='profile'),
    path('edit-user/', edit_user, name="edit_user"),
    path('accounts/change-pass/', change_password, name='change_password'),
    # Estas son parte de la clase de hoy, no del proyecto
    path('arrendadores/', solo_arrendadores, name='solo_arrendadores'),
    path('arrendatarios/', solo_arrendatarios, name='solo_arrendatarios'),
]