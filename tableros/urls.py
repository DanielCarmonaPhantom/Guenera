from django.urls import path, include, re_path

from . import views

app_name="tableros"
urlpatterns = [
    path('', views.index, name="index"), 
    path('<str:username>/', views.url_nan, name='url_nan'),
    path('<str:username>/blank/', views.blank, name='blank'),
    path('<str:username>/<slug:worktable_slug>/', views.url_class_nan, name='url_class_nan'),
    path('<str:username>/<slug:worktable_slug>/blank', views.create_class, name='create_class'),
    path('<str:username>/<slug:worktable_slug>/inscripccion/<slug:class_slug>/', views.class_inscription, name='class_inscription'),
    path('<str:username>/<slug:worktable_slug>/<slug:class_slug>/tablero', views.class_view, name='class_view'),
    path('<str:username>/<slug:worktable_slug>/<slug:class_slug>/alumnos', views.students_list, name='students_list'),
    path('<str:username>/<slug:worktable_slug>/<slug:class_slug>/alumnos/enroll_student/<int:id>', views.enroll_student, name='enroll_student'),
    path('<str:username>/<slug:worktable_slug>/<slug:class_slug>/alumnos/reject_student/<int:id>', views.reject_student, name='reject_student'),
    # path('<str:username>/<slug:worktable_slug>/<slug:class_slug>/', views.class_view, name='class_view')
]
