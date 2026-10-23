# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBytes, StrictStr
from typing import Tuple, Union
from typing_extensions import Annotated
from certiumet_stubs.models.conflicto import Conflicto
from certiumet_stubs.models.error import Error
from certiumet_stubs.security_api import get_token_tokenUsuario

class BaseCertificadosApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseCertificadosApi.subclasses = BaseCertificadosApi.subclasses + (cls,)
    async def descargar_certificado(
        self,
        id: Annotated[int, Field(ge=1, description="Identificador interno del pedido.")],
    ) -> bytes:
        """HU-04 · CA-04.1 a CA-04.3. Solo para pedidos propios en estado APROBADO. La descarga queda en la bitácora (E-04)."""
        ...
