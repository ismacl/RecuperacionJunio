from django.contrib import admin
from django.urls import path
from webserviceapp.views import buscar_equipos

urlpatterns = [
    path('equipos/', buscar_equipos, name='buscar_equipos'),
]
