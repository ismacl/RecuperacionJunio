"""
URL configuration for red_social project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webserviceapp.views import crear_aficionado
from webserviceapp.views import login
from webserviceapp.views import logout
from webserviceapp.views import username
from webserviceapp.views import obtener_equipos_seguidos
from webserviceapp.views import crear_equipo
from webserviceapp.views import agregar_comentario
from webserviceapp.views import comentarios_contenido
from webserviceapp.views import agregar_contenido_aficionado
from webserviceapp.views import eliminar_contenido
from webserviceapp.views import buscar_equipos


urlpatterns = [
    path('admin/', admin.site.urls),
    path('aficionado/', crear_aficionado, name='crear_aficionado'),
    path('session/', login),
    path('session/' , logout),
    path('users/<str:username>/', username, name='username'),
    path('aficionado/<int:id_aficionado>/equipos/', obtener_equipos_seguidos, name='equipos_seguidos'),
    path('equipos/', crear_equipo, name='crear_equipo'),
    path('agregar_comentario/', agregar_comentario, name='agregar_comentario'),
    path('contenido_aficionado/<int:id_contenido>/comentarios/', comentarios_contenido, name='comentarios_contenido'),
    path('contenido_aficionado/', agregar_contenido_aficionado, name='agregar_contenido_aficionado'),
    path('eliminarContenido/', eliminar_contenido, name='eliminar_contenido'),
    path('equipos/', buscar_equipos, name='buscar_equipos'),
]
