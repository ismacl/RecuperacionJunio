from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def crear_equipo(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Verificar si se proporcionaron los parámetros requeridos
            if 'equipo' not in data or 'liga' not in data or 'pais' not in data or 'año_fundacion' not in data or 'estadio' not in data or 'url_equipo' not in data:
                return JsonResponse({'error': 'Faltan parámetros o son incorrectos'}, status=400)

            # Crear un nuevo equipo
            nuevo_equipo = Equipo.objects.create(
                nombre=data['equipo'],
                liga=data['liga'],
                pais=data['pais'],
                año_fundacion=data['año_fundacion'],
                estadio=data['estadio'],
                url_equipo=data['url_equipo']
            )

            return JsonResponse({'message': 'Equipo creado exitosamente'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud no válida'}, status=400)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
