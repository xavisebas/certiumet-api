"""Adaptadores de Django para los puertos de solicitudes (ADR-003)."""

from __future__ import annotations

from contextlib import AbstractContextManager

from django.db import transaction

from solicitudes.dominio import Solicitud
from solicitudes.models import SolicitudModelo


def _a_dominio(m: SolicitudModelo) -> Solicitud:
    return Solicitud(
        id=m.id,
        numero_tramite=m.numero_tramite or "",
        estudiante_id=m.estudiante_id,
        tipo_certificado=m.tipo_certificado,
        estado=m.estado,
        fecha_creacion=m.fecha_creacion,
        motivo_rechazo=m.motivo_rechazo,
        codigo_verificacion=m.codigo_verificacion,
    )


class RepositorioSolicitudesDjango:
    def crear(self, estudiante_id: int, tipo_certificado: str) -> Solicitud:
        with transaction.atomic():
            m = SolicitudModelo.objects.create(estudiante_id=estudiante_id, tipo_certificado=tipo_certificado)
            m.numero_tramite = f"CERT-{m.fecha_creacion.year}-{m.id:06d}"
            m.save(update_fields=["numero_tramite"])
        return _a_dominio(m)

    def obtener(self, id_solicitud: int) -> Solicitud | None:
        m = SolicitudModelo.objects.filter(pk=id_solicitud).first()
        return _a_dominio(m) if m else None

    def obtener_para_actualizar(self, id_solicitud: int) -> Solicitud | None:
        # SELECT ... FOR UPDATE: bloqueo por fila de PostgreSQL (ADR-001).
        m = SolicitudModelo.objects.select_for_update().filter(pk=id_solicitud).first()
        return _a_dominio(m) if m else None

    def guardar(self, solicitud: Solicitud) -> None:
        SolicitudModelo.objects.filter(pk=solicitud.id).update(
            estado=solicitud.estado,
            motivo_rechazo=solicitud.motivo_rechazo,
            codigo_verificacion=solicitud.codigo_verificacion,
        )


class UnidadDeTrabajoDjango:
    def transaccion(self) -> AbstractContextManager[None]:
        return transaction.atomic()
