from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
def comentarios_contenido(request, id_contenido):
    if request.method == 'GET':
        try:
            # Obtener los comentarios asociados al contenido
            comentarios = Comentarios.objects.filter(Id_Contenido=id_contenido)
            if not comentarios.exists():
                return JsonResponse({'error': 'No hay comentarios para el contenido proporcionado.'}, status=404)

            # Preparar la lista de comentarios
            comentarios_info = [{
                'id_comentario': comentario.id_Comentarios,
                'id_aficionado': comentario.Id_aficionado.Id_aficionado,
                'username': comentario.Id_aficionado.UserName,
                'comentario': comentario.Comentario,
                'fecha_comentario': comentario.Fecha_comentario,
            } for comentario in comentarios]

            # Devolver la respuesta JSON con la lista de comentarios
            return JsonResponse(comentarios_info, safe=False, status=200)

        except Comentarios.DoesNotExist:
            # No se encontraron comentarios para el contenido con el ID proporcionado
            return JsonResponse({'error': f'No existe un contenido con el ID {id_contenido}'}, status=404)

        except Exception as e:
            # Otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
