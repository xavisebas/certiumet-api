"""HU-05 · CA-05.1 y CA-05.2 (E-03)."""

from __future__ import annotations

from pytest_bdd import given, scenarios, then, when
from rest_framework.test import APIClient

from apoyo import ESTUDIANTE_A, crear_pedido
from emision.models import Certificado
from solicitudes.dominio import Estado

scenarios("hu05.feature")

CANTIDAD = 100


def alterar(codigo: str, posicion: int) -> str:
    """Cambia un solo carácter de la firma (después del guion)."""
    indice = codigo.index("-") + 1 + (posicion % (len(codigo) - codigo.index("-") - 1))
    nuevo = "0" if codigo[indice] != "0" else "1"
    return codigo[:indice] + nuevo + codigo[indice + 1 :]


@given("100 certificados emitidos")
def cien_certificados(ctx):
    ids = [crear_pedido(ESTUDIANTE_A, Estado.APROBADO) for _ in range(CANTIDAD)]
    ctx["codigos"] = list(Certificado.objects.filter(solicitud_id__in=ids).values_list("codigo", flat=True))
    assert len(ctx["codigos"]) == CANTIDAD


@given("100 códigos de verificación con un carácter cambiado")
def cien_alterados(ctx):
    cien_certificados(ctx)
    ctx["codigos"] = [alterar(c, i) for i, c in enumerate(ctx["codigos"])]


@when("una entidad consulta cada código sin iniciar sesión")
@when("una entidad consulta cada código")
def consulta_codigos(ctx):
    cliente = APIClient()  # sin token: acceso público
    ctx["respuestas"] = [cliente.get(f"/api/v1/verificaciones/{c}") for c in ctx["codigos"]]


@then('la API responde 200 con "valido" en verdadero en los 100 casos')
def todos_validos(ctx):
    assert len(ctx["respuestas"]) == CANTIDAD
    assert all(r.status_code == 200 and r.json()["valido"] is True for r in ctx["respuestas"])


@then("muestra solo nombres, tipo de certificado y fecha de emisión, sin calificaciones")
def solo_datos_minimos(ctx):
    for r in ctx["respuestas"]:
        assert set(r.json()) == {"valido", "nombres", "tipoCertificado", "fechaEmision"}


@then('la API responde 200 con "valido" en falso en los 100 casos')
def todos_no_validos(ctx):
    assert len(ctx["respuestas"]) == CANTIDAD
    assert all(r.status_code == 200 and r.json()["valido"] is False for r in ctx["respuestas"])


@then("no muestra datos del estudiante")
def sin_datos(ctx):
    assert all(r.json() == {"valido": False} for r in ctx["respuestas"])
