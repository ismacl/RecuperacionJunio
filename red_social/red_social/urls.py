from django.contrib import admin
from django.urls import path
from webserviceapp.views import crear_aficionado

urlpatterns = [
    path('equipos/', views.buscar_equipos, name='buscar_equipos'),
]
