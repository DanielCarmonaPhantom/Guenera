from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import messages


from django.contrib.auth.models import User


from .forms import RegisterForm

def index(request):

    context = {
        'title' : 'Home'
    }

    if request.user.is_authenticated:
        return redirect('tableros:index')


    return render(request, 'home/index.html', context) 

def login_view(request):
    context = {
        'title' : 'Login'
    }

    if request.user.is_authenticated:
        return redirect('tableros:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password) #None
        

        if user: 
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            print("Usuario autenticado")
            return redirect('tableros:index', user)
        else:
            print("Usuario no autentificado")
            messages.error(request, 'Usuario o contraseña no validos')
            

    return render(request, 'home/login.html', context) 

def register_view(request):

    if request.user.is_authenticated:
        return redirect('tableros:index')


    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():        
        user = form.save()

        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('tableros:index', user)

    context = {
        'title': 'Registrarse',
        'form': form
    }
    return render(request, 'home/register.html', context)