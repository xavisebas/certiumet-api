"""Dominio del módulo de solicitudes.

Este archivo no depende de Django ni de la base de datos (ADR-003); la regla se
controla de forma automática con import-linter (archivo .importlinter).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


class Estado:
    EN_VALIDACION = "EN_VALIDACION"
    VALIDADO = "VALIDADO"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class Rol:
    ESTUDIANTE = "ESTUDIANTE"
    FUNCIONARIO = "FUNCIONARIO"


TIPOS_CERTIFICADO = ("MATRICULA", "CALIFICACIONES", "CULMINACION_ESTUDIOS")


class ErrorDominio(Exception):
    """Error esperado de una regla de negocio."""


class ConflictoEstado(ErrorDominio):
    def __init__(
        self, estado_actual: str, mensaje: str = "La acción no es posible en el estado actual del pedido."
    ) -> None:
        super().__init__(mensaje)
        self.estado_actual = estado_actual


class NoEncontrado(ErrorDominio):
    pass


class SinPermiso(ErrorDominio):
    pass


class DatosInvalidos(ErrorDominio):
    pass


class ServicioNoDisponible(ErrorDominio):
    """Un sistema externo necesario para completar la acción no respondió (E-06)."""


@dataclass(frozen=True)
class Usuario:
    id: int
    rol: str
    nombres: str

    @property
    def es_funcionario(self) -> bool:
        return self.rol == Rol.FUNCIONARIO


@dataclass
class Solicitud:
    id: int
    numero_tramite: str
    estudiante_id: int
    tipo_certificado: str
    estado: str
    fecha_creacion: datetime
    motivo_rechazo: str | None = None
    codigo_verificacion: str | None = None

    def pertenece_a(self, usuario: Usuario) -> bool:
        return self.estudiante_id == usuario.id

    def aprobar(self) -> None:
        if self.estado != Estado.VALIDADO:
            raise ConflictoEstado(self.estado, "Solo se puede aprobar un pedido en estado VALIDADO.")
        self.estado = Estado.APROBADO

    def rechazar(self, motivo: str | None) -> None:
        if not motivo or not motivo.strip():
            raise DatosInvalidos("El motivo es obligatorio al rechazar un pedido.")
        if self.estado != Estado.VALIDADO:
            raise ConflictoEstado(self.estado, "Solo se puede rechazar un pedido en estado VALIDADO.")
        self.estado = Estado.RECHAZADO
        self.motivo_rechazo = motivo.strip()

    def marcar_validado(self) -> None:
        if self.estado != Estado.EN_VALIDACION:
            raise ConflictoEstado(self.estado)
        self.estado = Estado.VALIDADO


def validar_tipo_certificado(tipo: object) -> str:
    if tipo not in TIPOS_CERTIFICADO:
        raise DatosInvalidos("El tipo de certificado no es válido.")
    return str(tipo)
