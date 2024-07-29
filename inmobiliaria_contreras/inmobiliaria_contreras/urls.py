from django.contrib import admin
from django.urls import path, include
from main.views import register, indexView, profile, edit_user, change_password
from inmuebles.views import nuevo_inmueble, crear_inmueble, editar_inmueble, eliminar_inmueble, detalleInmueble

urlpatterns = [
path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/change-pass/', change_password, name='change-password'),
    path('', indexView, name='home'),
    path('accounts/register/', register, name = 'register'),
    path('', include('main.urls')),
    path('edit-user/', edit_user, name='edit_user'),
    path('inmuebles/nuevo/', nuevo_inmueble, name='nuevo_inmueble'),
    path('inmuebles/crear/', crear_inmueble, name='crear_inmueble'),
    path('inmuebles/editar/<id>/', editar_inmueble, name='editar_inmueble'),
    path('inmuebles/eliminar/<id>/', eliminar_inmueble, name='eliminar_inmueble'),
    path('<id>/', detalleInmueble, name= 'detalle_inmueble')
    ]