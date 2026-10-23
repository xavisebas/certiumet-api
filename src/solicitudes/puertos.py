"""Puertos (interfaces) que necesitan los casos de uso de solicitudes (ADR-003).

Los adaptadores que los implementan con Django están en solicitudes/adaptadores.py,
emision/adaptadores.py y auditoria/adaptadores.py.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Protocol

from solicitudes.dominio import Solicitud


class RepositorioSolicitudes(Protocol):
    def crear(self, estudiante_id: int, tipo_certificado: str) -> Solicitud: ...

    def obtener(self, id_solicitud: int) -> Solicitud | None: ...

    def obtener_para_actualizar(self, id_solicitud: int) -> Solicitud | None:
        """Lee el pedido y lo bloquea hasta terminar la transacción (ADR-001)."""
        ...

    def guardar(self, solicitud: Solicitud) -> None: ...


class Bitacora(Protocol):
    def registrar(self, usuario_id: int | None, accion: str, recurso: str, ip: str | None) -> None: ...


class EmisorCertificados(Protocol):
    def emitir(self, solicitud: Solicitud) -> str:
        """Crea el único certificado del pedido y devuelve su código de verificación."""
        ...

    def generar_pdf(self, solicitud: Solicitud) -> bytes: ...


class UnidadDeTrabajo(Protocol):
    def transaccion(self) -> AbstractContextManager[None]: ...
