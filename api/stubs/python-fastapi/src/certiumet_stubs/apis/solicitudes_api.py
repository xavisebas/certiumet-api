# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from certiumet_stubs.apis.solicitudes_api_base import BaseSolicitudesApi
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

from pydantic import Field
from typing_extensions import Annotated
from certiumet_stubs.models.conflicto import Conflicto
from certiumet_stubs.models.error import Error
from certiumet_stubs.models.nueva_solicitud import NuevaSolicitud
from certiumet_stubs.models.resolucion import Resolucion
from certiumet_stubs.models.solicitud import Solicitud
from certiumet_stubs.models.extra_models import TokenModel  # noqa: F401
from certiumet_stubs.security_api import get_token_tokenUsuario

router = APIRouter()

ns_pkg = certiumet_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/solicitudes",
    responses={
        201: {"model": Solicitud, "description": "Pedido registrado."},
        401: {"model": Error, "description": "Falta el token o no es válido."},
        403: {"model": Error, "description": "El rol del usuario no permite esta acción."},
        422: {"model": Error, "description": "Los datos enviados no cumplen el contrato."},
    },
    tags=["Solicitudes"],
    summary="Pedir un certificado",
    response_model_by_alias=True,
)
async def crear_solicitud(
    nueva_solicitud: NuevaSolicitud = Body(..., description="", examples=[{"tipoCertificado": "MATRICULA"}]),
    token_tokenUsuario: TokenModel = Security(
        get_token_tokenUsuario
    ),
) -> Solicitud:
    """HU-01 · CA-01.1 y CA-01.2. Registra el pedido del estudiante que inició sesión. El pedido empieza en EN_VALIDACION hasta que el sistema académico confirme los requisitos (E-06)."""
    if not BaseSolicitudesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSolicitudesApi.subclasses[0]().crear_solicitud(nueva_solicitud)


@router.get(
    "/api/v1/solicitudes/{id}",
    responses={
        200: {"model": Solicitud, "description": "Estado del pedido."},
        401: {"model": Error, "description": "Falta el token o no es válido."},
        404: {"model": Error, "description": "El pedido no existe o no pertenece al usuario; no se indica cuál de los dos casos ocurre (E-01)."},
    },
    tags=["Solicitudes"],
    summary="Consultar el estado de un pedido propio",
    response_model_by_alias=True,
)
async def consultar_solicitud(
    id: Annotated[int, Field(ge=1, description="Identificador interno del pedido.")] = Path(..., description="Identificador interno del pedido.", ge=1, examples=[1]),
    token_tokenUsuario: TokenModel = Security(
        get_token_tokenUsuario
    ),
) -> Solicitud:
    """HU-02 · CA-02.1 y CA-02.2. Si el pedido no es del estudiante que consulta, la respuesta es 404 sin indicar si existe, y el intento queda en la bitácora (E-01, E-04)."""
    if not BaseSolicitudesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSolicitudesApi.subclasses[0]().consultar_solicitud(id)


@router.patch(
    "/api/v1/solicitudes/{id}/resolucion",
    responses={
        200: {"model": Solicitud, "description": "Pedido resuelto."},
        401: {"model": Error, "description": "Falta el token o no es válido."},
        403: {"model": Error, "description": "El rol del usuario no permite esta acción."},
        404: {"model": Error, "description": "El pedido no existe o no pertenece al usuario; no se indica cuál de los dos casos ocurre (E-01)."},
        409: {"model": Conflicto, "description": "La acción no es posible en el estado actual del pedido."},
        422: {"model": Error, "description": "Los datos enviados no cumplen el contrato."},
    },
    tags=["Solicitudes"],
    summary="Aprobar o rechazar un pedido",
    response_model_by_alias=True,
)
async def resolver_solicitud(
    id: Annotated[int, Field(ge=1, description="Identificador interno del pedido.")] = Path(..., description="Identificador interno del pedido.", ge=1, examples=[1]),
    resolucion: Resolucion = Body(..., description="", examples=[{"decision": "APROBAR"}]),
    token_tokenUsuario: TokenModel = Security(
        get_token_tokenUsuario
    ),
) -> Solicitud:
    """HU-03 · CA-03.1 a CA-03.4. Solo el funcionario de Secretaría puede resolver. Al aprobar se emite un único certificado; una segunda aprobación del mismo pedido recibe 409 con el estado actual (E-02, ADR-001)."""
    if not BaseSolicitudesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSolicitudesApi.subclasses[0]().resolver_solicitud(id, resolucion)
