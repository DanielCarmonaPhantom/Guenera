import string
import random
import datetime

from itertools import chain

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required


from users.models import User
from .models import WorkTable, Class, Announcements, InscriptionWorktable, InscriptionsClass, EnrolledStudents

from tableros.forms import WorkTableForm, ClassForm, AnnouncementForm, GenerateUrlForm, ClassRegister


# -------------------- Cuando Inicia Sesión ------------------------- #

@login_required(login_url='login')
def index(request):

    # worktable = WorkTable.objects.create(worktable_name = formWork.cleaned_data.get('worktable_name'), user_id = request.user)

    return redirect('tableros:blank', User.objects.get(pk=request.user.id).username)


# -------------------- Cuando pone su username pero no el tablero ------------------------- #

@login_required(login_url='login')
def url_nan(request, username):

    # worktable = WorkTable.objects.create(worktable_name = formWork.cleaned_data.get('worktable_name'), user_id = request.user)

    return redirect('tableros:blank', User.objects.get(pk=request.user.id).username)


# -------------------- Cuando No tiene tableros ------------------------- #

@login_required(login_url='login')
def blank(request, username):

    # VERIFICAMOS SI TIENE TABLEROS PROPIOS
    TABLEROS = WorkTable.objects.filter(user_id=request.user)

    if len(TABLEROS) > 0:
        return redirect('tableros:url_class_nan', request.user.username, TABLEROS.reverse()[0].worktable_slug)

    # Verificamos si esta inscrito a un tablero
    TABLEROS_INSCRITOS = InscriptionWorktable.objects.filter(
        inscription_user_id=request.user)

    id_wortable = TABLEROS_INSCRITOS.reverse()[0].inscription_worktable_id.id

    if len(TABLEROS_INSCRITOS) > 0:
        return redirect('tableros:url_class_nan', request.user.username, WorkTable.objects.get(id=id_wortable).worktable_slug)

    TITULO_PESTANIA = request.user.username + ' | Guenara'

    context = {
        'title': TITULO_PESTANIA,
        'username': request.user.username
    }

    formWorkTable = WorkTableForm(request.POST)
    context['formWorkTable'] = formWorkTable

    # Formulario para crear una worktable
    if request.method == 'POST' and formWorkTable.is_valid():
        imagen = formWorkTable.cleaned_data.get('imagen')

        if imagen == None:

            worktable_invite_url = ''.join(random.choice(
                string.ascii_letters + string.digits) for _ in range(8))
            worktable = WorkTable.objects.create(worktable_name=formWorkTable.cleaned_data.get(
                'worktable_name'), user_id=request.user, worktable_invite_url=worktable_invite_url)

            return redirect('tableros:url_class_nan', request.user.username, worktable.worktable_slug)

    return render(request, 'tableros/tablero_blanco.html', context)


""" Vista de un tablero pero no esta inscrito en alguna clase/no tiene clase si el tablero es suyo
@author Daniel Carmona

Parametros que recibe
----------
username: 
    String del usuario recibido en la petición
worktable_slug : 
    String del slug del worktable al que esta inscrito


Returns
-------
redirect('tableros:create_class', request.user.username, worktable_slug)
    Verificamos si al tablero que entro, es el suyo y pueda crear una clase

return render(request, 'tableros/tablero-invite.html', context)
    Si el tablero no es suyo pero se inscribio al tablero y le aparecen las clases disponibles
"""
# -------------------- Cuando Entra a un tablero pero sin clase------------------------- #


@login_required(login_url='login')
def url_class_nan(request, username, worktable_slug):

    # Cuando Entra a un tablero pero no es el dueño del tablero
    # Verificamos de quien es el tablero

    TABLEROS = WorkTable.objects.filter(
        user_id=request.user, worktable_slug=worktable_slug, )

    if len(TABLEROS) > 0:
        return redirect('tableros:create_class', request.user.username, worktable_slug)

    # El tablero no es suyo
    # Ahora veremos si estas inscrito

    INSCRIPCCIONES_TABLEROS = InscriptionWorktable.objects.filter(inscription_worktable_id=WorkTable.objects.get(
        worktable_slug=worktable_slug),    inscription_user_id=request.user)
    if len(INSCRIPCCIONES_TABLEROS) > 0:

        TITULO_PESTANIA = request.user.username + ' | Guenara'

        context = {
            'title': TITULO_PESTANIA,
            'username': request.user.username,
            'worktable_slug': worktable_slug,
        }

        # Obtener Todos los tableros en total
        TABLEROS_INSCRITOS = InscriptionWorktable.objects.filter(
            inscription_user_id=request.user)

        TABLEROS_PROPIOS = WorkTable.objects.filter(user_id=request.user)

        context['worktables'] = list(
            chain(TABLEROS_INSCRITOS, TABLEROS_PROPIOS))

        # Obtendremos las clases del tablero
        context['clases'] = Class.objects.filter(
            WorkTable_id=WorkTable.objects.get(worktable_slug=worktable_slug).id)

        return render(request, 'tableros/tablero-invite.html', context)

    return redirect('tableros:blank', User.objects.get(pk=request.user.id).username)


# -------------------- Cuando Entra a Tablero y clase blank ------------------------- #
@login_required(login_url='login')
def create_class(request, username, worktable_slug):

    # VERIFICAMOS SI TIENE CLASES
    CLASES = Class.objects.filter(user_id=request.user)

    if len(CLASES) > 0:
        return redirect('tableros:class_view', request.user.username, worktable_slug, CLASES.reverse()[0].class_slug)

    TITULO_PESTANIA = request.user.username + ' | Guenara'

    context = {
        'title': TITULO_PESTANIA,
        'username': request.user.username,

    }

    # Obtener los worktables de un usuario
    TABLEROS = WorkTable.objects.filter(user_id=request.user)

    context['worktables'] = TABLEROS

    formWorkTable = WorkTableForm(request.POST)
    formClass = ClassForm(request.POST)

    context['formWorkTable'] = formWorkTable
    context['formClass'] = formClass

    # Formulario para crear Worktable
    if request.method == 'POST' and formWorkTable.is_valid():
        imagen = formWorkTable.cleaned_data.get('imagen')

        if imagen == None:
            worktable = WorkTable.objects.create(worktable_name=formWorkTable.cleaned_data.get(
                'worktable_name'), user_id=request.user)
            return redirect('tableros:create_class', request.user.username, worktable.worktable_slug)

    # Formulario para crear una clase
    if request.method == 'POST' and formClass.is_valid():

        clase = Class.objects.create(
            class_name=formClass.cleaned_data.get('class_name'),
            class_description=formClass.cleaned_data.get('class_description'),
            WorkTable_id=WorkTable.objects.get(worktable_slug=worktable_slug),
            user_id=request.user
        )

        return redirect('tableros:class_view', request.user.username, worktable_slug, clase.class_slug)

    return render(request, 'tableros/tablero-class-blank.html', context)


""" Vista para cuando el usuario se va a inscribir a una clase o ve los detalles
@author Daniel Carmona

Parametros que recibe
----------
username: 
    String del usuario recibido en la petición
worktable_slug : 
    String del slug del worktable al que esta inscrito
class_slug :
    Strign del slug de la clase que esta viendo los detalles


Returns
-------
classes/class-inscription.html
    Template donde se visualiza los detalles el formulario de inscripcción
classes/class-request-sent.html
    Tempalte donde se visualiza que se ya se solicito unirse a una clase
"""


@login_required(login_url='login')
def class_inscription(request, username, worktable_slug, class_slug):

    TITULO_PESTANIA = request.user.username + ' | Guenara'

    context = {
        'title': TITULO_PESTANIA,
        'username': request.user.username,
        'worktable_slug': worktable_slug

    }
    # Obtener Todos los tableros para pintar en el aside
    TABLEROS_INSCRITOS = InscriptionWorktable.objects.filter(
        inscription_user_id=request.user)

    TABLEROS_PROPIOS = WorkTable.objects.filter(user_id=request.user)

    context['worktables'] = list(
        chain(TABLEROS_INSCRITOS, TABLEROS_PROPIOS))

    # Obtenemos el objeto de la clase actual
    CLASE = Class.objects.get(
        WorkTable_id=WorkTable.objects.get(worktable_slug=worktable_slug),
        class_slug=class_slug
    )

    context['clase'] = CLASE

    # Obtener datos del usario logeado
    USUARIO = request.user

    # context['user_name'] = USUARIO.
    context['user_email'] = USUARIO.email
    context['user_username'] = USUARIO.username

    # Verificamos si cuenta con alguna inscripccion a esa clase
    INSCRIPCCIONES = InscriptionsClass.objects.filter(
        student_id=request.user,
        class_id=CLASE
    )

    print(len(INSCRIPCCIONES))

    if len(INSCRIPCCIONES) > 0:

        # context['']
        # Verificamos el estatus de la inscripcción

        INSCRIPCION = INSCRIPCCIONES.reverse()[0]

        if INSCRIPCION.application_status == 'accepted':
            pass
        else:
            return render(request, 'classes/class-request-sent.html', context)

    # OBTENER FORMULARIO PARA REGISTRO

    formInscriptionClass = ClassRegister(request.POST)

    context['formInscriptionClass'] = formInscriptionClass

    if request.method == 'POST' and formInscriptionClass.is_valid():

        print("Validando formulario")

        InscriptionsClass.objects.create(
            student_name=formInscriptionClass.cleaned_data.get('student_name'),
            student_username=formInscriptionClass.cleaned_data.get(
                'student_username'),
            student_email=formInscriptionClass.cleaned_data.get(
                'student_email'),

            student_id=request.user,

            class_id=CLASE,
        )

        return render(request, 'classes/class-request-sent.html', context)

    return render(request, 'classes/class-inscription.html', context)


# -------------------- Cuando Crea una clase ------------------------- #

@login_required(login_url='login')
def class_view(request, username, worktable_slug, class_slug):

    TITULO_PESTANIA = request.user.username + ' | Guenara'

    context = {
        'title': TITULO_PESTANIA,
        'username': request.user.username
    }

    # OBTENER CANTIDAD DE TABLEROS Y CLASES
    TABLEROS = WorkTable.objects.filter(user_id=request.user)
    CLASES = Class.objects.filter(user_id=request.user)

    context['worktables'] = TABLEROS
    context['clases'] = CLASES

    # OBTENER DATOS DE WORKTABLE Y LA CLASE
    CLASE_SELECCIONADA = Class.objects.get(class_slug=class_slug)
    WORKTABLE_SELECCIONADO = WorkTable.objects.get(
        worktable_slug=worktable_slug)

    context['clase'] = CLASE_SELECCIONADA
    context['class_slug'] = CLASE_SELECCIONADA.class_slug

    context['worktable_selected'] = WORKTABLE_SELECCIONADO.worktable_name
    context['worktable_slug'] = WORKTABLE_SELECCIONADO.worktable_slug

    # OBTENER SUSCRIPCIÓN DE USUARIO LOGIN
    context['user_suscription'] = request.user.suscription

    # OBTENER FORMULARIO PARA POST DE CLASE

    formAnnouncement = AnnouncementForm(request.POST)
    formWorkTable = WorkTableForm(request.POST)
    formClass = ClassForm(request.POST)
    formGenerateUrl = GenerateUrlForm(request.POST)

    # CREAR UN ANUNCIO DE CLASE
    if request.method == 'POST' and formAnnouncement.is_valid():
        textoEditor = formAnnouncement.cleaned_data.get('class_name')

        Announcements.objects.create(
            announcement_text=textoEditor,
            announcement_class_id=CLASE_SELECCIONADA,
            announcement_worktable_id=WORKTABLE_SELECCIONADO,
            announcement_user_id=request.user,
            announcement_username=request.user.username
        )

    # SE COLOCAN LOS FORMS QUE IRAN A LA VISTA
    context['formAnnouncement'] = formAnnouncement
    context['formWorkTable'] = formWorkTable
    context['formClass'] = formClass
    context['formGenerateUrl'] = formGenerateUrl

    context['random_url'] = WORKTABLE_SELECCIONADO.worktable_invite_url

    # Formulario para cambiar fecha expiración el url
    if request.method == 'POST' and formGenerateUrl.is_valid():

        opcion = formGenerateUrl.cleaned_data.get(
            'worktable_invite_url_expiration')

        if opcion == 'A':
            days = datetime.timedelta(days=1)
        elif opcion == 'B':
            days = datetime.timedelta(days=3)
        else:
            days = datetime.timedelta(days=7)

        WORKTABLE_SELECCIONADO.worktable_invite_url_expiration = WORKTABLE_SELECCIONADO.worktable_invite_url_expiration + days

        WORKTABLE_SELECCIONADO.save()

    # Formulario para crear una clase
    if request.method == 'POST' and formClass.is_valid():

        clase = Class.objects.create(
            class_name=formClass.cleaned_data.get('class_name'),
            class_description=formClass.cleaned_data.get('class_description'),
            WorkTable_id=WorkTable.objects.get(worktable_slug=worktable_slug),
            user_id=request.user
        )

        return redirect('tableros:class_view', request.user.username, worktable_slug, clase.class_slug)

    # SE PINTAN LOS ANUNCIOS DE CLASES
    ANUNCIOS = reversed(Announcements.objects.filter(
        announcement_class_id=CLASE_SELECCIONADA,
        announcement_worktable_id=WORKTABLE_SELECCIONADO,
        announcement_user_id=request.user
    ))

    context['anuncios'] = ANUNCIOS

    return render(request, 'tableros/tablero.html', context)


""" Vista para visualizar las solicitudes de clase y los alumnos
@author Daniel Carmona

Parametros que recibe
----------
username: 
    String del usuario recibido en la petición
worktable_slug : 
    String del slug del worktable al que esta inscrito
class_slug :
    Strign del slug de la clase que esta viendo los detalles


Returns
-------

"""


@login_required(login_url='login')
def students_list(request, username, worktable_slug, class_slug):

    TITULO_PESTANIA = request.user.username + ' | Guenara'

    context = {
        'title': TITULO_PESTANIA,
        'username': request.user.username
    }

    # OBTENER CANTIDAD DE TABLEROS Y CLASES
    TABLEROS = WorkTable.objects.filter(user_id=request.user)
    CLASES = Class.objects.filter(user_id=request.user)

    context['worktables'] = TABLEROS
    context['clases'] = CLASES

    # OBTENER DATOS DE WORKTABLE Y LA CLASE
    CLASE_SELECCIONADA = Class.objects.get(class_slug=class_slug)
    WORKTABLE_SELECCIONADO = WorkTable.objects.get(
        worktable_slug=worktable_slug)

    context['clase'] = CLASE_SELECCIONADA
    context['class_slug'] = CLASE_SELECCIONADA.class_slug

    context['worktable_selected'] = WORKTABLE_SELECCIONADO.worktable_name
    context['worktable_slug'] = WORKTABLE_SELECCIONADO.worktable_slug

    # OBTENER LOS DATOS DE LAS SOLICITUDES DE CLASE
    SOLICITUDES = InscriptionsClass.objects.filter(class_id=CLASE_SELECCIONADA)

    context['count_class_requests'] = len(SOLICITUDES)
    context['class_requests'] = SOLICITUDES


    # OBTENER LOS DATOS DE LOS ALUMNOS YA INSCRITOS
    STUDENTS = EnrolledStudents.objects.filter(class_id=CLASE_SELECCIONADA)

    context['count_class_enrolled_students'] = len(STUDENTS)
    context['enrolled_students'] = STUDENTS

    # OBTENER SUSCRIPCIÓN DE USUARIO LOGIN
    context['user_suscription'] = request.user.suscription

    # OBTENER FORMULARIOS

    formAnnouncement = AnnouncementForm(request.POST)
    formWorkTable = WorkTableForm(request.POST)
    formGenerateUrl = GenerateUrlForm(request.POST)
    formClass = ClassForm(request.POST)

    # SE COLOCAN LOS FORMS QUE IRAN A LA VISTA
    context['formAnnouncement'] = formAnnouncement
    context['formWorkTable'] = formWorkTable
    context['formGenerateUrl'] = formGenerateUrl
    context['formClass'] = formClass

    context['random_url'] = WORKTABLE_SELECCIONADO.worktable_invite_url

    # Formulario para cambiar fecha expiración el url
    if request.method == 'POST' and formGenerateUrl.is_valid():

        opcion = formGenerateUrl.cleaned_data.get(
            'worktable_invite_url_expiration')

        if opcion == 'A':
            days = datetime.timedelta(days=1)
        elif opcion == 'B':
            days = datetime.timedelta(days=3)
        else:
            days = datetime.timedelta(days=7)

        WORKTABLE_SELECCIONADO.worktable_invite_url_expiration = WORKTABLE_SELECCIONADO.worktable_invite_url_expiration + days

        WORKTABLE_SELECCIONADO.save()

    # Formulario para crear una clase
    if request.method == 'POST' and formClass.is_valid():

        clase = Class.objects.create(
            class_name=formClass.cleaned_data.get('class_name'),
            class_description=formClass.cleaned_data.get('class_description'),
            WorkTable_id=WorkTable.objects.get(worktable_slug=worktable_slug),
            user_id=request.user
        )

        return redirect('tableros:class_view', request.user.username, worktable_slug, clase.class_slug)

    return render(request, 'tableros/student-list.html', context)


""" Vista para eliminar una solicitud a una clase
@author Daniel Carmona

Parametros que recibe
----------
username: 
    String del usuario recibido en la petición
worktable_slug : 
    String del slug del worktable al que esta inscrito
class_slug :
    Strign del slug de la clase que esta viendo los detalles


Returns
-------

"""


@login_required(login_url='login')
def enroll_student(request, id, username, worktable_slug, class_slug):

    INSCRIPCION = InscriptionsClass.objects.get(id=id)

    EnrolledStudents.objects.create(
        student_id=User.objects.get(id=INSCRIPCION.student_id.id),
        class_id=Class.objects.get(id=INSCRIPCION.class_id.id)

    )

    INSCRIPCION.delete()

    return redirect('tableros:students_list', request.user.username, worktable_slug, class_slug)


@login_required(login_url='login')
def reject_student(request, id, username, worktable_slug, class_slug):

    INSCRIPCION = InscriptionsClass.objects.get(id=id)
    INSCRIPCION.application_status = 'rejected'
    INSCRIPCION.save()


    return redirect('tableros:students_list', request.user.username, worktable_slug, class_slug)
