"""HU-01 · CA-01.1 a CA-01.4. CA-01.3 (@carga) se excluye: es la prueba de carga de E-07."""

from __future__ import annotations

from pytest_bdd import given, parsers, scenarios, then, when

from integracion_academica import fabrica
from integracion_academica.adaptador_simulado import AdaptadorAcademicoSimulado
from solicitudes.dominio import Estado
from solicitudes.models import SolicitudModelo

scenarios("hu01.feature")

TIPOS = {"certificado de matrícula": "MATRICULA"}


@given("el sistema académico no responde")
def sistema_academico_caido(monkeypatch, ctx):
    monkeypatch.setattr(fabrica, "AdaptadorAcademicoSimulado", lambda: AdaptadorAcademicoSimulado(disponible=False))
    ctx["sistema_caido"] = True


@when(parsers.parse('pide un "{tipo}"'))
def pide_certificado(ctx, tipo):
    ctx["respuesta"] = ctx["cliente"].post("/api/v1/solicitudes", {"tipoCertificado": TIPOS[tipo]}, format="json")
    if ctx["respuesta"].status_code == 201:
        ctx["id"] = ctx["respuesta"].json()["id"]


@when("pide un tipo de certificado que no existe")
def pide_tipo_inexistente(ctx):
    ctx["respuesta"] = ctx["cliente"].post("/api/v1/solicitudes", {"tipoCertificado": "INEXISTENTE"}, format="json")


@then("la respuesta trae un número de trámite")
def trae_numero_tramite(ctx):
    numero = ctx["respuesta"].json()["numeroTramite"]
    assert numero.startswith("CERT-") and len(numero) == len("CERT-2026-000001")


@then("no se guarda ningún pedido")
def no_se_guarda(ctx):
    assert SolicitudModelo.objects.count() == 0


@then('el pedido queda en estado "EN_VALIDACION" para validarse más tarde')
def queda_para_validar(ctx):
    assert ctx["sistema_caido"]
    assert SolicitudModelo.objects.get(pk=ctx["id"]).estado == Estado.EN_VALIDACION
