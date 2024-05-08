from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseConflict
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionado, Equipos, Aficionado, Comentarios
import json

@csrf_exempt
def agregar_comentario(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Verificar si se proporcionaron los parámetros requeridos
            if 'id_aficionado' not in data or 'id_contenido' not in data or 'comentario' not in data or 'fecha_publicacion' not in data:
                return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

            # Verificar si el aficionado y el contenido existen
            if not Aficionado.objects.filter(id_aficionado=data['id_aficionado']).exists() or not Contenido.objects.filter(id_contenido=data['id_contenido']).exists():
                return HttpResponseBadRequest('El aficionado o el contenido no existen', content_type='text/plain')

            # Crear el comentario
            nuevo_comentario = Comentario(
                id_aficionado=data['id_aficionado'],
                id_contenido=data['id_contenido'],
                comentario=data['comentario'],
                fecha_publicacion=datetime.strptime(data['fecha_publicacion'], '%d-%m-%Y').date()
            )
            nuevo_comentario.save()

            return JsonResponse({'message': 'Comentario agregado exitosamente'}, status=201)

        except KeyError:
            # Faltan parámetros en la solicitud
            return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

        except Exception as e:
            # Otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
