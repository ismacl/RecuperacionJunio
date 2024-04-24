from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def username(request, username):
    if request.method == 'GET':
        # Recuperar el aficionado por su nombre de usuario
        try:
            aficionado = Aficionado.objects.get(username=username)

            # Verificar si el aficionado tiene un token de sesión válido
            if not aficionado.Token_Sesion:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

            # Obtener la información del perfil del aficionado
            perfil = {
                'username': aficionado.UserName,
                'url_avatar': aficionado.url_avatar,
                'description': aficionado.Description,
                'equipos': aficionado.Equipos
            }

            return JsonResponse(perfil, status=200)

        except Aficionado.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
