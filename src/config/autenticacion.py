"""Autenticación con token JWT simulado (supuesto A2).

En un caso real el token lo entrega el sistema de usuarios de la universidad. En el
proyecto se firma con una clave local y lleva el identificador interno del usuario,
su rol y sus nombres; nunca la cédula (R1).
"""

from dataclasses import dataclass

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from solicitudes.dominio import Usuario


@dataclass(frozen=True)
class UsuarioAutenticado:
    """Envoltura que DRF necesita (is_authenticated) alrededor del usuario de dominio."""

    usuario: Usuario

    @property
    def is_authenticated(self) -> bool:
        return True


def emitir_token(usuario_id: int, rol: str, nombres: str) -> str:
    """Genera un token de prueba. Solo se usa en desarrollo y en las pruebas."""
    datos = {"sub": str(usuario_id), "rol": rol, "nombres": nombres}
    return jwt.encode(datos, settings.JWT_CLAVE, algorithm="HS256")


class AutenticacionToken(authentication.BaseAuthentication):
    def authenticate(self, request):
        cabecera = request.headers.get("Authorization", "")
        if not cabecera.startswith("Bearer "):
            return None
        token = cabecera.removeprefix("Bearer ").strip()
        try:
            datos = jwt.decode(token, settings.JWT_CLAVE, algorithms=["HS256"])
            usuario = Usuario(id=int(datos["sub"]), rol=datos["rol"], nombres=datos["nombres"])
        except (jwt.PyJWTError, KeyError, ValueError) as error:
            raise exceptions.AuthenticationFailed("Token no válido.") from error
        return UsuarioAutenticado(usuario), token

    def authenticate_header(self, request) -> str:
        return "Bearer"
