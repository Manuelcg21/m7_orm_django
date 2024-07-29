from django import forms
from inmuebles.forms import InmuebleForm

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput())
    passRepeat = forms.CharField(widget = forms.PasswordInput())