"""Adaptador del puerto EmisorCertificados y verificación pública (CU-05)."""

from __future__ import annotations

from django.conf import settings

from emision.dominio import firmar, leer_codigo
from emision.models import Certificado
from emision.pdf import generar_pdf
from integracion_academica.fabrica import crear_proveedor
from integracion_academica.puerto import ProveedorDatosAcademicos
from solicitudes.dominio import Solicitud


class EmisorDjango:
    def __init__(self, proveedor: ProveedorDatosAcademicos, clave: str) -> None:
        self.proveedor = proveedor
        self.clave = clave

    def emitir(self, solicitud: Solicitud) -> str:
        datos = self.proveedor.obtener_estudiante(solicitud.estudiante_id)
        certificado = Certificado.objects.create(
            solicitud_id=solicitud.id,
            tipo_certificado=solicitud.tipo_certificado,
            nombres_titular=datos.nombres,
        )
        certificado.codigo = firmar(certificado.id, self.clave)
        certificado.save(update_fields=["codigo"])
        return certificado.codigo

    def generar_pdf(self, solicitud: Solicitud) -> bytes:
        certificado = Certificado.objects.get(solicitud_id=solicitud.id)
        notas = self.proveedor.obtener_calificaciones(solicitud.estudiante_id, solicitud.tipo_certificado)
        lineas = [
            "Universidad - Secretaria General",
            f"Certificado de {certificado.tipo_certificado.replace('_', ' ').lower()}",
            f"Titular: {certificado.nombres_titular}",
            f"Fecha de emision: {certificado.fecha_emision.isoformat()}",
            *[f"{n.asignatura}: {n.nota}" for n in notas],
            f"Codigo de verificacion: {certificado.codigo}",
        ]
        return generar_pdf(lineas)

    def verificar(self, codigo: str) -> dict:
        id_certificado = leer_codigo(codigo, self.clave)
        certificado = Certificado.objects.filter(pk=id_certificado, codigo=codigo).first() if id_certificado else None
        if certificado is None:
            return {"valido": False}
        return {
            "valido": True,
            "nombres": certificado.nombres_titular,
            "tipoCertificado": certificado.tipo_certificado,
            "fechaEmision": certificado.fecha_emision.isoformat(),
        }


def crear_emisor() -> EmisorDjango:
    return EmisorDjango(crear_proveedor(), settings.CLAVE_FIRMA_CERTIFICADOS)
