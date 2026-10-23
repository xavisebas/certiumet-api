"""Vistas HTTP de solicitudes (adaptador de entrada). Solo traducen HTTP ↔ casos de uso."""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auditoria.adaptadores import BitacoraDjango
from emision.adaptadores import crear_emisor
from solicitudes import casos_uso
from solicitudes.adaptadores import RepositorioSolicitudesDjango, UnidadDeTrabajoDjango
from solicitudes.dominio import DatosInvalidos, Solicitud


def a_json(s: Solicitud) -> dict:
    """Convierte la solicitud al esquema Solicitud del contrato."""
    return {
        "id": s.id,
        "numeroTramite": s.numero_tramite,
        "tipoCertificado": s.tipo_certificado,
        "estado": s.estado,
        "fechaCreacion": s.fecha_creacion.isoformat().replace("+00:00", "Z"),
        "motivoRechazo": s.motivo_rechazo,
        "codigoVerificacion": s.codigo_verificacion,
    }


def ip_de(request) -> str | None:
    return request.META.get("REMOTE_ADDR")


def leer_cuerpo(request, permitidos: set[str]) -> dict:
    if not isinstance(request.data, dict):
        raise DatosInvalidos("El cuerpo debe ser un objeto JSON.")
    sobrantes = set(request.data) - permitidos
    if sobrantes:
        raise DatosInvalidos(f"Campos no permitidos: {', '.join(sorted(sobrantes))}.")
    return request.data


class SolicitudesVista(APIView):
    def post(self, request):
        datos = leer_cuerpo(request, {"tipoCertificado"})
        solicitud = casos_uso.crear_solicitud(
            request.user.usuario,
            datos.get("tipoCertificado"),
            RepositorioSolicitudesDjango(),
            BitacoraDjango(),
            ip_de(request),
        )
        return Response(a_json(solicitud), status=status.HTTP_201_CREATED)


class SolicitudDetalleVista(APIView):
    def get(self, request, id: int):
        solicitud = casos_uso.consultar_solicitud(
            request.user.usuario, id, RepositorioSolicitudesDjango(), BitacoraDjango(), ip_de(request)
        )
        return Response(a_json(solicitud))


class ResolucionVista(APIView):
    def patch(self, request, id: int):
        datos = leer_cuerpo(request, {"decision", "motivo"})
        solicitud = casos_uso.resolver_solicitud(
            request.user.usuario,
            id,
            datos.get("decision"),
            datos.get("motivo"),
            RepositorioSolicitudesDjango(),
            BitacoraDjango(),
            crear_emisor(),
            UnidadDeTrabajoDjango(),
            ip_de(request),
        )
        return Response(a_json(solicitud))
