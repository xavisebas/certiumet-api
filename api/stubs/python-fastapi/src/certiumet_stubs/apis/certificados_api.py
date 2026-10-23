# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from certiumet_stubs.apis.certificados_api_base import BaseCertificadosApi
import certiumet_stubs.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from pydantic import Field, StrictBytes, StrictStr
from typing import Tuple, Union
from typing_extensions import Annotated
from certiumet_stubs.models.conflicto import Conflicto
from certiumet_stubs.models.error import Error
from certiumet_stubs.models.extra_models import TokenModel  # noqa: F401
from certiumet_stubs.security_api import get_token_tokenUsuario

router = APIRouter()

ns_pkg = certiumet_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/api/v1/solicitudes/{id}/certificado",
    responses={
        200: {"model": bytes, "description": "Certificado en PDF."},
        401: {"model": Error, "description": "Falta el token o no es válido."},
        404: {"model": Error, "description": "El pedido no existe o no pertenece al usuario; no se indica cuál de los dos casos ocurre (E-01)."},
        409: {"model": Conflicto, "description": "La acción no es posible en el estado actual del pedido."},
    },
    tags=["Certificados"],
    summary="Descargar el certificado en PDF",
    response_model_by_alias=True,
)
async def descargar_certificado(
    id: Annotated[int, Field(ge=1, description="Identificador interno del pedido.")] = Path(..., description="Identificador interno del pedido.", ge=1, examples=[1]),
    token_tokenUsuario: TokenModel = Security(
        get_token_tokenUsuario
    ),
) -> bytes:
    """HU-04 · CA-04.1 a CA-04.3. Solo para pedidos propios en estado APROBADO. La descarga queda en la bitácora (E-04)."""
    if not BaseCertificadosApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCertificadosApi.subclasses[0]().descargar_certificado(id)
