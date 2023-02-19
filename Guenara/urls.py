
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.views.static import serve

from . import views


urlpatterns = [
    path('', views.index, name="index"),  
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='register'),
    path('tableros/', include('tableros.urls'), name='tableros'),
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]