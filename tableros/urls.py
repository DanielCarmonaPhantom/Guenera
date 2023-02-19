
from django.urls import path

from . import views

app_name="tableros"
urlpatterns = [
    path('', views.index, name="index"), 
    path('logout', views.logout_view, name='logout'), 
]
