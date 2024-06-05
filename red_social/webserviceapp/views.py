from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Aficionados, Equipos, Contenido, Comentarios
import json

@csrf_exempt
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
            datos_respuesta = {'Token_Sesion': nuevo_token_sesion}
            return JsonResponse(datos_respuesta, status=201)

        except Usuario.DoesNotExist:
            return HttpResponseUnauthorized('Usuario no encontrado', content_type='text/plain')

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
            data = json.loads(request.body)
            Token_Sesion = data.get('sessionToken')

            # Verificar si se proporcionó un token de sesión válido
            if not Token_Sesion:
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

@csrf_exempt
def obtener_equipos_seguidos(request, id_aficionado):
    try:
        aficionado = Aficionado.objects.get(id_aficionado=id_aficionado)
        equipos_seguidos = aficionado.equipos.all()
        
        if equipos_seguidos:
            data = []
            for equipo in equipos_seguidos:
                data.append({
                    'equipo': equipo.nombre,
                    'liga': equipo.liga,
                    'pais': equipo.pais,
                    'año_fundacion': equipo.año_fundacion,
                    'estadio': equipo.estadio,
                    'url_equipo': equipo.url_equipo
                })
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({'error': 'No se encontraron equipos seguidos para este usuario'}, status=404)
    
    except Aficionado.DoesNotExist:
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
    
@csrf_exempt
def eliminar_contenido(request, id_contenido):
    if request.method == 'DELETE':
        token = request.headers.get('Token_Sesion')

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
