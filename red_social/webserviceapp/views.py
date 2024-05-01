from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def obtener_equipos_seguidos(request, id_aficionado):
    try:
        aficionado = Aficionado.objects.get(id_aficionado=id_aficionado)
        equipos_seguidos = aficionado.equipos.all()
        
        if equipos_seguidos:
            data = []
            for equipo in equipos_seguidos:
                data.append({
                    'equipo': equipo.nombre,
                    'liga': equipo.liga,
                    'pais': equipo.pais,
                    'año_fundacion': equipo.año_fundacion,
                    'estadio': equipo.estadio,
                    'url_equipo': equipo.url_equipo
                })
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({'error': 'No se encontraron equipos seguidos para este usuario'}, status=404)
    
    except Aficionado.DoesNotExist:
        return JsonResponse({'error': 'El usuario no existe'}, status=404)
