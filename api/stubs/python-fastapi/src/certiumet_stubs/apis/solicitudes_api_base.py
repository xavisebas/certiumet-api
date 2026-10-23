# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing_extensions import Annotated
from certiumet_stubs.models.conflicto import Conflicto
from certiumet_stubs.models.error import Error
from certiumet_stubs.models.nueva_solicitud import NuevaSolicitud
from certiumet_stubs.models.resolucion import Resolucion
from certiumet_stubs.models.solicitud import Solicitud
from certiumet_stubs.security_api import get_token_tokenUsuario

class BaseSolicitudesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSolicitudesApi.subclasses = BaseSolicitudesApi.subclasses + (cls,)
    async def crear_solicitud(
        self,
        nueva_solicitud: NuevaSolicitud,
    ) -> Solicitud:
        """HU-01 · CA-01.1 y CA-01.2. Registra el pedido del estudiante que inició sesión. El pedido empieza en EN_VALIDACION hasta que el sistema académico confirme los requisitos (E-06)."""
        ...


    async def consultar_solicitud(
        self,
        id: Annotated[int, Field(ge=1, description="Identificador interno del pedido.")],
    ) -> Solicitud:
        """HU-02 · CA-02.1 y CA-02.2. Si el pedido no es del estudiante que consulta, la respuesta es 404 sin indicar si existe, y el intento queda en la bitácora (E-01, E-04)."""
        ...


    async def resolver_solicitud(
        self,
        id: Annotated[int, Field(ge=1, description="Identificador interno del pedido.")],
        resolucion: Resolucion,
    ) -> Solicitud:
        """HU-03 · CA-03.1 a CA-03.4. Solo el funcionario de Secretaría puede resolver. Al aprobar se emite un único certificado; una segunda aprobación del mismo pedido recibe 409 con el estado actual (E-02, ADR-001)."""
        ...
