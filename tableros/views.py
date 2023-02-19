from django.shortcuts import render, redirect


from django.contrib import messages
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .forms import WorkTableForm
from .models import WorkTable

@login_required(login_url='login')
def index(request):

    context = {
        'title' : 'Tableros'
    }


    formWork = WorkTableForm()
    context['form'] = formWork

    print("-------------------------")
    print(formWork)
    print(formWork.is_valid())

    if request.method == 'POST' and formWork.is_valid(): 

        print("Formulario valido")

        WorkTable.objects.create_user(
            form.cleaned_data.get('worktable_name'),
            form.cleaned_data.get('imagen'),
            request.user
        )

    
    return render(request, 'tableros/index.html', context) 

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitoxamente')
    return redirect('login')