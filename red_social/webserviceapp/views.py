from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def agregar_contenido_aficionado(request):
    if request.method == 'POST':
        try:
            # Verificar si el token es válido (esta función debería estar definida y manejar la lógica de verificación de token)
            error_response, token_payload = verificar_token(request)
            if error_response:
                return error_response

            # Verificar que el token pertenece al usuario
            data = json.loads(request.body)
            if token_payload['id_aficionado'] != data['id_aficionado']:
                return JsonResponse({'error': 'No autorizado. El token no pertenece al usuario'}, status=401)

            # Verificar que se proporcionaron todos los parámetros requeridos
            required_fields = ['id_aficionado', 'tipo_contenido', 'url_contenido', 'descripcion']
            if not all(field in data for field in required_fields):
                return HttpResponseBadRequest('Faltan parámetros o son incorrectos')

            # Buscar al aficionado por el ID proporcionado
            aficionado = Aficionado.objects.get(Id_aficionado=data['id_aficionado'])

            # Crear el nuevo contenido
            nuevo_contenido = Contenido(
                Id_aficionado=aficionado,
                Tipo_Contenido=data['tipo_contenido'],
                URL=data['url_contenido'],
                Descripcion=data['descripcion'],
                Fecha_Publicacion=datetime.date.today()
            )
            nuevo_contenido.save()

            # Devolver la respuesta con éxito
            return JsonResponse({'message': 'Contenido creado exitosamente'}, status=201)

        except Aficionado.DoesNotExist:
            return JsonResponse({'error': 'Aficionado no encontrado'}, status=404)

        except KeyError:
            # Faltan parámetros en la solicitud
            return HttpResponseBadRequest('Faltan parámetros o son incorrectos')

        except Exception as e:
            # Otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
