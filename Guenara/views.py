from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User


from .forms import RegisterForm

from users.models import User
from tableros.models import WorkTable, InscriptionWorktable


def index(request):

    context = {
        'title' : 'Home | Guenara'
    }

    # if request.user.is_authenticated:
        # return redirect('tableros:index')


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
            return redirect('tableros:index')
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
            return redirect('tableros:index')

    context = {
        'title': 'Registrarse',
        'form': form
    }
    return render(request, 'home/register.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitoxamente')
    return redirect('login')


def invite(request, worktable_invite_url):

    ## VERIFICAMOS SI EL CÓDIGO DE INVITACIÓN EXISTE

    try:
        ## Si esta login redirigir

        ## No login

        ## OBTENER NOMBRE DE TABLERO Y USUARIO 
        TABLERO = WorkTable.objects.get(worktable_invite_url= worktable_invite_url)
        USUARIO = User.objects.get(email=TABLERO.user_id)


        TITULO_PESTANIA = ' Guenara'

        context = {
            'title': TITULO_PESTANIA,
            'username_invite' : USUARIO.username,
            'worktable_name' : TABLERO.worktable_name

        }

        form = RegisterForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():        
            user = form.save()

            if user:
                login(request, user)
                messages.success(request, 'Usuario creado exitosamente')
                InscriptionWorktable.objects.create(inscription_worktable_id = TABLERO, inscription_user_id= user)

                return redirect('tableros:url_class_nan', user.username, TABLERO.worktable_slug)
            

        context['form'] = form

        return render(request, 'home/register-invitation.html', context)



    except Exception as e:
       ## NO EXISTE LA INVITACIÓN 
        
        print(e)
        
        print("Sali")


    
        return render(request, 'home/register.html')