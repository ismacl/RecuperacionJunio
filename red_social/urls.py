from django.contrib import admin
from django.urls import path
from webserviceapp.views import crear_aficionado

urlpatterns = [
    path('contenido_aficionado/<int:id_contenido>/', views.eliminar_contenido, name='eliminar_contenido'),

]
