from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def buscar_equipos(request):
    if request.method == 'GET':
        # Recuperar los parámetros de la solicitud
        equipo = request.GET.get('equipo')
        liga = request.GET.get('liga')
        pais = request.GET.get('pais')
        año_fundacion = request.GET.get('año_fundacion')
        estadio = request.GET.get('estadio')
        url_equipo = request.GET.get('url_equipo')

        # Construir el filtro dinámico
        filtros = {}
        if equipo:
            filtros['Nombre'] = equipo
        if liga:
            filtros['Liga'] = liga
        if pais:
            filtros['Pais'] = pais
        if año_fundacion:
            filtros['Año_Fundacion'] = año_fundacion
        if estadio:
            filtros['Estadio'] = estadio
        if url_equipo:
            filtros['url_equipo'] = url_equipo

        # Filtrar los equipos según los parámetros proporcionados
        equipos = Equipos.objects.filter(**filtros)
        
        # Construir la respuesta
        equipos_list = []
        for equipo in equipos:
            equipos_list.append({
                "equipo": equipo.Nombre,
                "liga": equipo.Liga,
                "pais": equipo.Pais,
                "año_fundacion": equipo.Año_Fundacion,
                "estadio": equipo.Estadio,
                "url_equipo": equipo.url_equipo,
            })

        return JsonResponse(equipos_list, safe=False, status=200)
    
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
