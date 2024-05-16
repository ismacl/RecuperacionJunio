from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Verificar si se proporcionaron los parámetros requeridos
            if 'username' not in data or 'password' not in data:
                return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

            # Buscar al usuario por el nombre de usuario proporcionado
            aficionado = Aficionado.objects.get(Username=data['username'])

            # Verificar si la contraseña es correcta
            if not check_password(data['password'], aficionado.password):
                return HttpResponse('Contraseña incorrecta', status=401,  content_type='text/plain')

            # Generar un nuevo token de sesión y actualizar el usuario
            nuevo_token_sesion = crear_token(id_aficionado)
            usuario.token_sesion = nuevo_token_sesion
            usuario.save()

            # Devolver la respuesta con el token de sesión
            datos_respuesta = {'token_sesion': nuevo_token_sesion}
            return JsonResponse(datos_respuesta, status=201)

        except Usuario.DoesNotExist:
            return HttpResponseUnauthorized('Usuario no encontrado', content_type='text/plain')

def crear_aficionado(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos de la solicitud de crear usuario
            data = json.loads(request.body)

            # Verificar si ya existe un usuario con el mismo email
            if Usuario.objects.filter(email=data['email']).exists():
                return HttpResponseConflict('Ya existe un usuario con ese email', content_type='text/plain')

            # Crear un nuevo aficionado
            with transaction.atomic():
                nuevo_aficionado = Usuario(
                    id_aficionado=data['id_aficionado'],
                    username=data['username'],
                    password=make_password(data['password']),
                    email=data['email'],
                    birthdate=data['birthdate'],
                    Token_Sesion='',
                    url_avatar=data['url_avatar']
                )
                nuevo_aficionado.save()

            return JsonResponse({'mensaje': 'Aficionado creado exitosamente'}, status=201)

        except KeyError:
            # Faltan parámetros en la solicitud
            return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

        except Exception as e:
            # Otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
