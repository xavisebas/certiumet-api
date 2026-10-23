"""HU-04 · CA-04.1 a CA-04.3 (E-01, E-04)."""

from __future__ import annotations

from pytest_bdd import given, scenarios, then, when

from apoyo import ESTUDIANTE_B, crear_pedido, registro_completo
from auditoria.models import RegistroAuditoria
from solicitudes.dominio import Estado

scenarios("hu04.feature")


def ruta(id_solicitud: int) -> str:
    return f"/api/v1/solicitudes/{id_solicitud}/certificado"


@when("descarga el certificado")
@when("intenta descargar el certificado")
@when("el estudiante A intenta descargarlo")
def descarga(ctx):
    ctx["respuesta"] = ctx["cliente"].get(ruta(ctx["id"]))


@then("la API responde 200 con un archivo PDF")
def responde_pdf(ctx):
    assert ctx["respuesta"].status_code == 200
    assert ctx["respuesta"]["Content-Type"] == "application/pdf"
    assert ctx["respuesta"].content.startswith(b"%PDF-")


@then("la descarga queda en la bitácora con sus cinco campos")
def descarga_en_bitacora(ctx):
    registro = RegistroAuditoria.objects.get(accion="DESCARGAR_CERTIFICADO", recurso=f"solicitud:{ctx['id']}")
    assert registro_completo(registro)


@then("no se entrega ningún archivo")
def sin_archivo(ctx):
    assert ctx["respuesta"]["Content-Type"] == "application/json"


@given("un certificado emitido para el estudiante B")
def certificado_de_b(ctx):
    ctx["id"] = crear_pedido(ESTUDIANTE_B, Estado.APROBADO)


@then("el intento queda guardado en la bitácora")
def intento_en_bitacora(ctx):
    registro = RegistroAuditoria.objects.get(accion="ACCESO_DENEGADO", recurso=f"solicitud:{ctx['id']}")
    assert registro.usuario_id == 101
    assert registro_completo(registro)
