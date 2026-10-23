# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from certiumet_stubs.models.conflicto import Conflicto  # noqa: F401
from certiumet_stubs.models.error import Error  # noqa: F401
from certiumet_stubs.models.nueva_solicitud import NuevaSolicitud  # noqa: F401
from certiumet_stubs.models.resolucion import Resolucion  # noqa: F401
from certiumet_stubs.models.solicitud import Solicitud  # noqa: F401


def test_crear_solicitud(client: TestClient):
    """Test case for crear_solicitud

    Pedir un certificado
    """
    nueva_solicitud = {"tipoCertificado":"MATRICULA"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1/solicitudes",
    #    headers=headers,
    #    json=nueva_solicitud,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_consultar_solicitud(client: TestClient):
    """Test case for consultar_solicitud

    Consultar el estado de un pedido propio
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/v1/solicitudes/{id}".format(id=1),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_resolver_solicitud(client: TestClient):
    """Test case for resolver_solicitud

    Aprobar o rechazar un pedido
    """
    resolucion = {"decision":"APROBAR"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PATCH",
    #    "/api/v1/solicitudes/{id}/resolucion".format(id=1),
    #    headers=headers,
    #    json=resolucion,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

