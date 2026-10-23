# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from certiumet_stubs.apis.verificaciones_api_base import BaseVerificacionesApi
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
from certiumet_stubs.models.verificacion import Verificacion

router = APIRouter()

ns_pkg = certiumet_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/api/v1/verificaciones/{codigo}",
    responses={
        200: {"model": Verificacion, "description": "Resultado de la verificación (válido o no válido)."},
    },
    tags=["Verificaciones"],
    summary="Verificar la autenticidad de un certificado",
    response_model_by_alias=True,
)
async def verificar_certificado(
    codigo: Annotated[str, Field(min_length=10, max_length=80, description="Código de verificación impreso en el certificado.")] = Path(..., description="Código de verificación impreso en el certificado.", min_length=10, max_length=80, examples=["7-3f9a1c2b7d4e8f60a1b2"]),
) -> Verificacion:
    """HU-05 · CA-05.1 y CA-05.2. Acceso público sin iniciar sesión. Muestra solo nombres, tipo de certificado y fecha de emisión; nunca calificaciones (E-03, R1)."""
    if not BaseVerificacionesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseVerificacionesApi.subclasses[0]().verificar_certificado(codigo)
