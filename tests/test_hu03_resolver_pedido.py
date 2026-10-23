"""HU-03 · CA-03.1 a CA-03.4. CA-03.2 es la prueba de concurrencia de E-02 (tarea T07)."""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from django.db import connection
from pytest_bdd import given, parsers, scenarios, then, when

from apoyo import ESTUDIANTE_A, FUNCIONARIO_1, FUNCIONARIO_2, cliente_para, crear_pedido, registro_completo
from auditoria.models import RegistroAuditoria
from emision.models import Certificado
from solicitudes.dominio import Estado
from solicitudes.models import SolicitudModelo

scenarios("hu03.feature")

PARES = 1000
HILOS = 16


def ruta(id_solicitud: int) -> str:
    return f"/api/v1/solicitudes/{id_solicitud}/resolucion"


@given(parsers.parse('un pedido en estado "{estado}"'))
def pedido_en_estado(ctx, estado):
    ctx["id"] = crear_pedido(ESTUDIANTE_A, estado)


@when("un funcionario lo aprueba")
def funcionario_aprueba(ctx):
    ctx["respuesta"] = cliente_para(FUNCIONARIO_1).patch(ruta(ctx["id"]), {"decision": "APROBAR"}, format="json")


@then("se emite un solo certificado con código de verificación")
def un_certificado(ctx):
    certificados = Certificado.objects.filter(solicitud_id=ctx["id"])
    assert certificados.count() == 1
    assert ctx["respuesta"].json()["codigoVerificacion"] == certificados.get().codigo


@then("la aprobación queda en la bitácora con usuario, acción, recurso, fecha y hora, y dirección IP")
def aprobacion_en_bitacora(ctx):
    registro = RegistroAuditoria.objects.get(accion="RESOLVER_APROBAR", recurso=f"solicitud:{ctx['id']}")
    assert registro.usuario_id == FUNCIONARIO_1.id
    assert registro_completo(registro)


# --- CA-03.2 · Concurrencia (E-02) ---------------------------------------------------


@given('1 000 pedidos en estado "VALIDADO"')
def mil_pedidos_validados(ctx):
    if connection.vendor != "postgresql":
        pytest.skip("La prueba de concurrencia de E-02 necesita PostgreSQL (ADR-001).")
    ctx["ids"] = [crear_pedido(ESTUDIANTE_A, Estado.VALIDADO) for _ in range(PARES)]


def _aprobar(id_solicitud: int, funcionario, barrera: Barrier) -> tuple[int, int, dict]:
    cliente = cliente_para(funcionario)
    try:
        barrera.wait(timeout=60)  # las dos aprobaciones del par salen al mismo tiempo
        respuesta = cliente.patch(ruta(id_solicitud), {"decision": "APROBAR"}, format="json")
        return id_solicitud, respuesta.status_code, respuesta.json()
    finally:
        connection.close()


@when("dos funcionarios aprueban cada pedido al mismo tiempo")
def aprobaciones_simultaneas(ctx):
    with ThreadPoolExecutor(max_workers=HILOS) as hilos:
        futuros = []
        for id_solicitud in ctx["ids"]:
            barrera = Barrier(2)
            futuros.append(hilos.submit(_aprobar, id_solicitud, FUNCIONARIO_1, barrera))
            futuros.append(hilos.submit(_aprobar, id_solicitud, FUNCIONARIO_2, barrera))
        ctx["resultados"] = [f.result() for f in futuros]


@then("hay 0 certificados duplicados")
def cero_duplicados(ctx):
    por_pedido = Counter(Certificado.objects.filter(solicitud_id__in=ctx["ids"]).values_list("solicitud_id", flat=True))
    duplicados = sum(1 for veces in por_pedido.values() if veces > 1)
    print(f"\n[E-02] pares={PARES} certificados={sum(por_pedido.values())} duplicados={duplicados}")
    assert duplicados == 0
    assert len(por_pedido) == PARES


@then("en los 1 000 pares, la aprobación que llega segunda recibe 409 con el estado actual del pedido")
def segundas_con_409(ctx):
    por_pedido: dict[int, list] = {}
    for id_solicitud, codigo, cuerpo in ctx["resultados"]:
        por_pedido.setdefault(id_solicitud, []).append((codigo, cuerpo))
    conflictos = 0
    for respuestas in por_pedido.values():
        codigos = sorted(c for c, _ in respuestas)
        assert codigos == [200, 409], codigos
        cuerpo_409 = next(b for c, b in respuestas if c == 409)
        assert cuerpo_409["estadoActual"] == Estado.APROBADO
        conflictos += 1
    print(f"[E-02] segundas aprobaciones con 409: {conflictos}/{PARES}")
    assert conflictos == PARES


# --- CA-03.3 y CA-03.4 ---------------------------------------------------------------


@when(parsers.parse('un funcionario lo rechaza con el motivo "{motivo}"'))
def funcionario_rechaza(ctx, motivo):
    ctx["respuesta"] = cliente_para(FUNCIONARIO_1).patch(
        ruta(ctx["id"]), {"decision": "RECHAZAR", "motivo": motivo}, format="json"
    )


@then("no se emite ningún certificado")
def sin_certificado(ctx):
    assert not Certificado.objects.filter(solicitud_id=ctx["id"]).exists()


@when("intenta aprobar un pedido")
def estudiante_intenta_aprobar(ctx):
    ctx["id"] = crear_pedido(ESTUDIANTE_A, Estado.VALIDADO)
    ctx["respuesta"] = ctx["cliente"].patch(ruta(ctx["id"]), {"decision": "APROBAR"}, format="json")


@then("el pedido no cambia de estado")
def no_cambia(ctx):
    assert SolicitudModelo.objects.get(pk=ctx["id"]).estado == Estado.VALIDADO
