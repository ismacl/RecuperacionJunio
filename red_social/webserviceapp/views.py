from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from .models import Aficionados, Equipos, Contenido, Comentarios
import json
import jwt

# Create your views here.

SECRET_KEY = 'clavesegurisima'

# Crear token

def crear_token(user_id):
	payload = {
		'user_id':user_id,
		'exp':datetime.utcnow() + timedelta(days=1),
		'iat':datetime.utcnow()
	}
	token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
	return token

# Verificar token

def verificar_token(request):
	token = request.META.get('HTTP_AUTHORIZATION', None)

	if not token:
		return JsonResponse({'error': 'Token no encontrado'}, status=401), None

	try:
		if token.startswith('Bearer '):
			token = token.split(' ')[1]

		payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
		return None, payload
	except jwt.ExpiredSignatureError:
		return JsonResponse({'error': 'Token expirado'}, status=401), None
	except jwt.InvalidTokenError:
		return JsonResponse({'error': 'Token invalido'}, status=401), None

@csrf_exempt
def crear_aficionado(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos de la solicitud de crear usuario
            data = json.loads(request.body)

            # Verificar si ya existe un usuario con el mismo email
            if Aficionados.objects.filter(gmail=data['gmail']).exists():
                return JsonResponse({'error': 'Ya existe un usuario'}, status="400")

            # Crear un nuevo aficionado
            with transaction.atomic():
                nuevo_aficionado = Aficionados(
                    id_aficionado=data['id_aficionado'],
                    username=data['username'],
                    password=make_password(data['password']),
                    gmail=data['gmail'],
                    birthdate=data['birthdate'],
                    token_sesion=None,
                    registerdate=data['registerdate'],
                    id_equipo=data['id_equipo'],
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
    

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Verificar si se proporcionaron los parámetros requeridos
            if 'username' not in data or 'password' not in data:
                return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

            # Buscar al usuario por el nombre de usuario proporcionado
            aficionado = Aficionados.objects.get(username=data['username'])

            # Verificar si la contraseña es correcta
            if not check_password(data['password'], aficionado.password):
                return HttpResponse('Contraseña incorrecta', status=401,  content_type='text/plain')

            # Generar un nuevo token de sesión y actualizar el usuario
            nuevo_token_sesion = crear_token(aficionado.id_aficionado)
            aficionado.token_sesion = nuevo_token_sesion
            aficionado.save()

            # Devolver la respuesta con el token de sesión
            datos_respuesta = {'Token_Sesion': nuevo_token_sesion}
            return JsonResponse(datos_respuesta, status=201)

        except aficionado.DoesNotExist:
            return HttpResponseNotFound('Usuario no encontrado', content_type='text/plain')

        except KeyError:
            # Faltan parámetros en la solicitud
            return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

        except Exception as e:
            # Otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def logout(request):
    if request.method == 'PATCH':
        try:
            # Recuperar el token de sesión del cuerpo de la solicitud
            Token_Sesion= request.META.get('HTTP_AUTHORIZATION', None)

            # Verificar si se proporcionó un token de sesión válido
            if not Token_Sesion:
                return HttpResponseBadRequest('Falta el token de sesión en la solicitud', content_type='text/plain')
                
            if Token_Sesion.startswith('Bearer '):
                Token_Sesion=Token_Sesion.split(' ')[1]

            # Buscar al aficionado con el token de sesión proporcionado
            aficionado = Aficionados.objects.get(token_sesion=Token_Sesion)

            # Limpiar el token de sesión del aficionado para cerrar la sesión
            aficionado.token_sesion = None
            aficionado.save()

            # Devolver una respuesta indicando que la sesión se ha cerrado correctamente
            return JsonResponse({'message': 'Sesión cerrada correctamente'}, status=200)

        except aficionado.DoesNotExist:
            # Manejar el caso en el que no se encuentra al aficionado con el token de sesión proporcionado
            return JsonResponse('Token de sesión no válido', content_type='text/plain')

        except Exception as e:
            # Manejar otros errores
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def username(request, username):
    if request.method == 'GET':
        # Recuperar el aficionado por su nombre de usuario
        try:
            aficionado = Aficionados.objects.get(username=username)

            # Verificar si el aficionado tiene un token de sesión válido
            if not aficionado.token_sesion:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

            # Obtener la información del perfil del aficionado
            perfil = {
                'username': aficionado.username,
                'url_avatar': aficionado.url_avatar,
                'equipos': aficionado.id_equipo
            }

            return JsonResponse(perfil, status=200)

        except Aficionados.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_equipos_seguidos(request, id_aficionado):
    try:
        aficionado = Aficionados.objects.get(id_aficionado=id_aficionado)

        id_equipo= aficionado.id_equipo
        
        if Equipos.objects.get(id_equipo=id_equipo):
           equipo=Equipos.objects.get(id_equipo=id_equipo)
           data = {
                    'equipo': equipo.nombre,
                    'liga': equipo.liga,
                    'pais': equipo.pais,
                    'año_fundacion': equipo.año_fundacion,
                    'estadio': equipo.estadio,
                    'url_equipo': equipo.url_equipo
            }
           
           return JsonResponse({'data': data})

        else:
            return JsonResponse({'error': 'No se encontraron equipos seguidos para este usuario'}, status=404)
    
    except Aficionados.DoesNotExist:
        return JsonResponse({'error': 'El usuario no existe'}, status=404)
    
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
            nuevo_equipo = Equipos.objects.create(
                nombre=data['equipo'],
                id_equipo=data['id_equipo'],
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
    
@csrf_exempt
def agregar_comentario(request):
    if request.method == 'POST':
        try:
            # Recuperar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Verificar si se proporcionaron los parámetros requeridos
            if 'id_aficionado' not in data or 'id_contenido' not in data or 'comentario' not in data or 'fecha_comentario' not in data:
                return HttpResponseBadRequest('Faltan parámetros o son incorrectos', content_type='text/plain')

            # Verificar si el aficionado y el contenido existen
            if not Aficionados.objects.filter(id_aficionado=data['id_aficionado']).exists() or not Contenido.objects.filter(id_contenido=data['id_contenido']).exists():
                return HttpResponseBadRequest('El aficionado o el contenido no existen', content_type='text/plain')
            
            id_contenido=Contenido.objects.get(id_contenido=data['id_contenido'])
            id_aficionado=Aficionados.objects.get(id_aficionado=data['id_aficionado'])

            # Crear el comentario
            nuevo_comentario = Comentarios(
                id_comentarios=data["id_comentarios"],
                id_aficionado=id_aficionado,
                id_contenido=id_contenido,
                comentario=data['comentario'],
                fecha_comentario=data['fecha_comentario']
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
    
@csrf_exempt
def comentarios_contenido(request, id_contenido):
    if request.method == 'GET':
        try:
            # Obtener los comentarios asociados al contenido
            comentarios = Comentarios.objects.filter(id_contenido=id_contenido)
            if not comentarios.exists():
                return JsonResponse({'error': 'No hay comentarios para el contenido proporcionado.'}, status=404)

            # Preparar la lista de comentarios
            comentarios_info = [{
                'id_comentario': comentario.id_comentarios,
                'id_aficionado': comentario.id_aficionado.id_aficionado,
                'username': comentario.id_aficionado.username,
                'comentario': comentario.comentario,
                'fecha_comentario': comentario.fecha_comentario,
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
            print(token_payload['user_id'])
            if token_payload['user_id'] != data['id_aficionado']:
                return JsonResponse({'error': 'No autorizado. El token no pertenece al usuario'}, status=401)

            # Buscar al aficionado por el ID proporcionado
            aficionado = Aficionados.objects.get(id_aficionado='1').id_aficionado

            # Crear el nuevo contenido
            nuevo_contenido = Contenido(
                id_aficionado=aficionado,
                tipo_contenido=data['tipo_contenido'],
                url=data['url_contenido'],
                descripcion=data['descripcion'],
                fecha_publicacion=['fecha_publicacion']
            )
            nuevo_contenido.save()

            # Devolver la respuesta con éxito
            return JsonResponse({'message': 'Contenido creado exitosamente'}, status=201)

        except Aficionados.DoesNotExist:
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
    
@csrf_exempt
def eliminar_contenido(request, id_contenido):
    if request.method == 'DELETE':
        token = request.META.get('HTTP_AUTHORIZATION', None)

        # Verificación del token de sesión

        if not token:
            return JsonResponse({'error': 'Token de sesión no proporcionado'}, status=401)

        try:
            aficionado = Aficionados.objects.get(Token_Sesion=token)
        except Aficionados.DoesNotExist:
            return JsonResponse('No autorizado. Token de sesión inválido o no proporcionado.', content_type='text/plain')

        # Verificación del contenido
        contenido = get_object_or_404(Contenido, pk=id_contenido, Id_aficionado=aficionado.id_aficionado)

        # Eliminación del contenido
        contenido.delete()
        return JsonResponse({'message': 'Contenido eliminado exitosamente'}, status=200)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def buscar_equipos(request):
    if request.method == 'GET':
        # Recuperar los parámetros de la solicitud
        equipo = request.GET.get('equipo', None)
        liga = request.GET.get('liga', None)
        pais = request.GET.get('pais', None)
        año_fundacion = request.GET.get('año_fundacion', None)
        estadio = request.GET.get('estadio', None)
        url_equipo = request.GET.get('url_equipo', None)

        # Construir el filtro dinámico
        filtros = {}
        if equipo:
            filtros['nombre__icontains'] = equipo
        if liga:
            filtros['liga__icontains'] = liga
        if pais:
            filtros['pais__icontains'] = pais
        if año_fundacion:
            filtros['año_fundacion'] = año_fundacion
        if estadio:
            filtros['estadio__icontains'] = estadio
        if url_equipo:
            filtros['url_equipo__icontains'] = url_equipo

        # Filtrar los equipos según los parámetros proporcionados
        equipos = Equipos.objects.filter(**filtros)
        
        # Construir la respuesta
        equipos_list = []
        for equipo in equipos:
            equipos_list.append({
                "equipo": equipo.nombre,
                "liga": equipo.liga,
                "pais": equipo.pais,
                "año_fundacion": equipo.año_fundacion,
                "estadio": equipo.estadio,
                "url_equipo": equipo.url_equipo,
            })

        return JsonResponse(equipos_list, safe=False, status=200)
    
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)