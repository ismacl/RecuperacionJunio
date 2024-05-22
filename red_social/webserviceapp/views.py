from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
@csrf_exempt
def eliminar_contenido(request, id_contenido):
    if request.method == 'DELETE':
        token = request.headers.get('SessionToken')

        # Verificación del token de sesión
        try:
            aficionado = Aficionado.objects.get(Token_Sesion=token)
        except Aficionado.DoesNotExist:
            return HttpResponseUnauthorized('No autorizado. Token de sesión inválido o no proporcionado.', content_type='text/plain')

        # Verificación del contenido
        contenido = get_object_or_404(Contenido, pk=id_contenido, Id_aficionado=aficionado.Id_aficionado)

        # Eliminación del contenido
        contenido.delete()
        return JsonResponse({'message': 'Contenido eliminado exitosamente'}, status=200)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
