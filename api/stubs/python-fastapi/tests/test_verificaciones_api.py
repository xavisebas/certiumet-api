# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from certiumet_stubs.models.verificacion import Verificacion  # noqa: F401


def test_verificar_certificado(client: TestClient):
    """Test case for verificar_certificado

    Verificar la autenticidad de un certificado
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/v1/verificaciones/{codigo}".format(codigo='7-3f9a1c2b7d4e8f60a1b2'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

