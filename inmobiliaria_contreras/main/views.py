from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.services import editar_user_sin_password
from django.contrib import messages

# Create your views here.
def success(req):
  return render(req, 'exito.html')

def form_test(req):
  return render(req, 'form_test_html')

@login_required
def index(req):
  return render(req, 'index.html')

@login_required
def home(req):
  return render(req, 'home.html')

@login_required
def profile(req):
  return render(req, 'profile.html')

@login_required
def edit_user(req):
  # 1. Obtengo el usuario actual
  current_user = req.user
  # llamo a la funcionpara editar usuario
  if req.POST['telefono'] != '':
    # trailing whitespaces .strip()
    editar_user_sin_password(current_user.username, 
                            req.POST['first_name'], 
                            req.POST['last_name'], 
                            req.POST['email'], 
                            req.POST['direccion'], 
                            req.POST['rol'],
                            req.POST['telefono'])
  else:
    editar_user_sin_password(current_user.username, 
                            req.POST['first_name'], 
                            req.POST['last_name'], 
                            req.POST['email'], 
                            req.POST['direccion'],
                            req.POST['rol'])
  messages.success(req, "Ha actualizado sus datos con éxito")
  return redirect('/')

def change_password(req):
  # 1. Recibo los datos del formulario
  password = req.POST['password']
  pass_repeat = req.POST['pass_repeat']
  # 2. Valido que ambas contraseñas coincidan
  if password != pass_repeat:
    messages.error(req, 'Las contraseñas no coinciden')
    return redirect('/accounts/profile')
  # 3. Actualizamos la contraseña
  req.user.set_password(password)
  req.user.save()
  # 4. Le avisamos al usuario que el cambio fué exitoso
  messages.success(req, 'Contraseña actualizada')
  return redirect('/accounts/profile')

# pendientes para trabajar con grupos
def solo_arrendadores(req):
  return HttpResponse('sólo arrendadores')

def solo_arrendatarios(req):
  return HttpResponse('sólo arrendatarios')