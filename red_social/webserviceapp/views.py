from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def logout(request):
    if request.method == 'PATCH':
        try:
            # Recuperar el token de sesión del cuerpo de la solicitud
            data = json.loads(request.body)
            session_token = data.get('sessionToken')

            # Verificar si se proporcionó un token de sesión válido
            if not session_token:
                return HttpResponseBadRequest('Falta el token de sesión en la solicitud', content_type='text/plain')

            # Buscar al aficionado con el token de sesión proporcionado
            aficionado = Aficionado.objects.get(Token_Sesion=session_token)

            # Limpiar el token de sesión del aficionado para cerrar la sesión
            aficionado.Token_Sesion = None
            aficionado.save()

            # Devolver una respuesta indicando que la sesión se ha cerrado correctamente
            return JsonResponse({'message': 'Sesión cerrada correctamente'}, status=200)

        except aficionado.DoesNotExist:
            # Manejar el caso en el que no se encuentra al aficionado con el token de sesión proporcionado
            return HttpResponseUnauthorized('Token de sesión no válido', content_type='text/plain')

        except Exception as e:
            # Manejar otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
