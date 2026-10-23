"""Pasos comunes de las pruebas derivadas de los criterios (07).

Los .feature de tests/features se generan desde docs/07-historias-y-criterios.md con
scripts/extraer_features.py, para que el criterio y la prueba tengan el mismo texto.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, then

from apoyo import ESTUDIANTE_A, cliente_para, crear_pedido
from solicitudes.models import SolicitudModelo


def pytest_collection_modifyitems(items):
    """Todas las pruebas usan la base de datos. Las de concurrencia (@E-02) necesitan
    transacciones reales entre hilos, por eso usan transaction=True."""
    for item in items:
        concurrente = item.get_closest_marker("E-02") is not None
        item.add_marker(pytest.mark.django_db(transaction=concurrente))


@pytest.fixture
def ctx() -> dict:
    return {}


# --- Pasos comunes ---------------------------------------------------------------


@given("un estudiante con sesión iniciada")
@given("un estudiante A con sesión iniciada")
def estudiante_con_sesion(ctx):
    ctx["usuario"] = ESTUDIANTE_A
    ctx["cliente"] = cliente_para(ESTUDIANTE_A)


@given("un estudiante con un pedido registrado")
def estudiante_con_pedido(ctx):
    estudiante_con_sesion(ctx)
    ctx["id"] = crear_pedido(ESTUDIANTE_A)


@given(parsers.parse('un estudiante con un pedido en estado "{estado}"'))
def estudiante_con_pedido_en_estado(ctx, estado):
    estudiante_con_sesion(ctx)
    ctx["id"] = crear_pedido(ESTUDIANTE_A, estado)


@then(parsers.parse("la API responde {codigo:d}"))
def api_responde(ctx, codigo):
    assert ctx["respuesta"].status_code == codigo, ctx["respuesta"].content


@then(parsers.parse('el pedido queda en estado "{estado}"'))
def pedido_en_estado(ctx, estado):
    assert SolicitudModelo.objects.get(pk=ctx["id"]).estado == estado
