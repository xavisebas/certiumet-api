"""HU-02 · CA-02.1 y CA-02.2 (E-01, E-04)."""

from __future__ import annotations

from pytest_bdd import given, scenarios, then, when

from apoyo import ESTUDIANTE_B, crear_pedido, registro_completo
from auditoria.models import RegistroAuditoria

scenarios("hu02.feature")


@when("consulta ese pedido")
def consulta_pedido(ctx):
    ctx["respuesta"] = ctx["cliente"].get(f"/api/v1/solicitudes/{ctx['id']}")


@then("la respuesta muestra el estado del pedido")
def muestra_estado(ctx):
    assert ctx["respuesta"].json()["estado"] == "EN_VALIDACION"


@given("200 pedidos que pertenecen a otros estudiantes")
def pedidos_ajenos(ctx):
    ctx["ajenos"] = [crear_pedido(ESTUDIANTE_B) for _ in range(200)]


@when("el estudiante A intenta consultar cada uno de esos pedidos")
def consulta_ajenos(ctx):
    ctx["respuestas"] = [ctx["cliente"].get(f"/api/v1/solicitudes/{i}") for i in ctx["ajenos"]]
    # Referencia: respuesta para un pedido que no existe.
    ctx["inexistente"] = ctx["cliente"].get("/api/v1/solicitudes/999999")


@then("la API responde 404 en los 200 intentos, sin indicar si el pedido existe")
def todos_404(ctx):
    assert len(ctx["respuestas"]) == 200
    assert all(r.status_code == 404 for r in ctx["respuestas"])
    # El cuerpo es idéntico al de un pedido inexistente: no revela que existe.
    assert all(r.json() == ctx["inexistente"].json() for r in ctx["respuestas"])


@then("se devuelven 0 calificaciones")
def cero_calificaciones(ctx):
    for r in ctx["respuestas"]:
        cuerpo = r.content.decode().lower()
        assert "nota" not in cuerpo and "calificacion" not in cuerpo


@then("los 200 intentos quedan guardados en la bitácora")
def intentos_en_bitacora(ctx):
    recursos = {f"solicitud:{i}" for i in ctx["ajenos"]}
    registros = RegistroAuditoria.objects.filter(accion="ACCESO_DENEGADO", recurso__in=recursos, usuario_id=101)
    assert registros.count() == 200
    assert all(registro_completo(r) for r in registros)
