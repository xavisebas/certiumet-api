"""Datos y funciones de apoyo para las pruebas (datos ficticios, supuesto A4)."""

from __future__ import annotations

from rest_framework.test import APIClient

from auditoria.models import RegistroAuditoria
from config.autenticacion import emitir_token
from solicitudes import casos_uso
from solicitudes.adaptadores import RepositorioSolicitudesDjango, UnidadDeTrabajoDjango
from solicitudes.dominio import Estado, Rol, Usuario
from solicitudes.models import SolicitudModelo

ESTUDIANTE_A = Usuario(id=101, rol=Rol.ESTUDIANTE, nombres="Ana Pérez")
ESTUDIANTE_B = Usuario(id=202, rol=Rol.ESTUDIANTE, nombres="Luis Andrade")
FUNCIONARIO_1 = Usuario(id=900, rol=Rol.FUNCIONARIO, nombres="Funcionario Uno")
FUNCIONARIO_2 = Usuario(id=901, rol=Rol.FUNCIONARIO, nombres="Funcionario Dos")


def cliente_para(usuario: Usuario | None) -> APIClient:
    cliente = APIClient()
    if usuario is not None:
        token = emitir_token(usuario.id, usuario.rol, usuario.nombres)
        cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return cliente


def crear_pedido(estudiante: Usuario, estado: str = Estado.EN_VALIDACION, tipo: str = "MATRICULA") -> int:
    """Crea un pedido y lo lleva al estado pedido usando los mismos casos de uso de la API."""
    solicitud = RepositorioSolicitudesDjango().crear(estudiante.id, tipo)
    if estado in (Estado.VALIDADO, Estado.APROBADO, Estado.RECHAZADO):
        SolicitudModelo.objects.filter(pk=solicitud.id).update(estado=Estado.VALIDADO)
    if estado in (Estado.APROBADO, Estado.RECHAZADO):
        from auditoria.adaptadores import BitacoraDjango
        from emision.adaptadores import crear_emisor

        decision = casos_uso.APROBAR if estado == Estado.APROBADO else casos_uso.RECHAZAR
        casos_uso.resolver_solicitud(
            FUNCIONARIO_1,
            solicitud.id,
            decision,
            "motivo de prueba",
            RepositorioSolicitudesDjango(),
            BitacoraDjango(),
            crear_emisor(),
            UnidadDeTrabajoDjango(),
            "127.0.0.1",
        )
    return solicitud.id


def registro_completo(registro: RegistroAuditoria) -> bool:
    """Los cinco campos de E-04: usuario, acción, recurso, fecha y hora, dirección IP."""
    return all(
        [registro.usuario_id, registro.accion, registro.recurso, registro.fecha_hora, registro.ip],
    )
