"""Vistas HTTP de certificados (CU-04) y verificación pública (CU-05)."""

from __future__ import annotations

from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auditoria.adaptadores import BitacoraDjango
from emision.adaptadores import crear_emisor
from solicitudes import casos_uso
from solicitudes.adaptadores import RepositorioSolicitudesDjango
from solicitudes.vistas import ip_de


class CertificadoVista(APIView):
    def get(self, request, id: int):
        pdf = casos_uso.descargar_certificado(
            request.user.usuario, id, RepositorioSolicitudesDjango(), BitacoraDjango(), crear_emisor(), ip_de(request)
        )
        respuesta = HttpResponse(pdf, content_type="application/pdf")
        respuesta["Content-Disposition"] = f'attachment; filename="certificado-{id}.pdf"'
        return respuesta


class VerificacionVista(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, request, codigo: str):
        return Response(crear_emisor().verificar(codigo))
