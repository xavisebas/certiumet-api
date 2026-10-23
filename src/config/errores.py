"""Convierte los errores de dominio y de DRF al esquema Error del contrato."""

from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from solicitudes.dominio import ConflictoEstado, DatosInvalidos, NoEncontrado, SinPermiso


def manejar_excepcion(exc, context):
    if isinstance(exc, ConflictoEstado):
        return Response(
            {"codigo": "CONFLICTO_ESTADO", "mensaje": str(exc), "estadoActual": exc.estado_actual},
            status=status.HTTP_409_CONFLICT,
        )
    if isinstance(exc, NoEncontrado):
        return Response(
            {"codigo": "NO_ENCONTRADO", "mensaje": "Pedido no encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if isinstance(exc, SinPermiso):
        return Response({"codigo": "SIN_PERMISO", "mensaje": str(exc)}, status=status.HTTP_403_FORBIDDEN)
    if isinstance(exc, DatosInvalidos):
        return Response(
            {"codigo": "DATOS_INVALIDOS", "mensaje": str(exc)},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    if isinstance(exc, exceptions.ParseError):
        return Response(
            {"codigo": "DATOS_INVALIDOS", "mensaje": "El cuerpo no es un JSON válido."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
        respuesta = Response(
            {"codigo": "NO_AUTENTICADO", "mensaje": "Se requiere iniciar sesión."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
        respuesta["WWW-Authenticate"] = "Bearer"
        return respuesta
    return exception_handler(exc, context)
