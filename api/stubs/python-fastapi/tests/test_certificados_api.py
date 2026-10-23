# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from certiumet_stubs.models.conflicto import Conflicto  # noqa: F401
from certiumet_stubs.models.error import Error  # noqa: F401


def test_descargar_certificado(client: TestClient):
    """Test case for descargar_certificado

    Descargar el certificado en PDF
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/v1/solicitudes/{id}/certificado".format(id=1),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

