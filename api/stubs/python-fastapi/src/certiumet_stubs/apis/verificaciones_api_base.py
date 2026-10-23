# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing_extensions import Annotated
from certiumet_stubs.models.verificacion import Verificacion


class BaseVerificacionesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseVerificacionesApi.subclasses = BaseVerificacionesApi.subclasses + (cls,)
    async def verificar_certificado(
        self,
        codigo: Annotated[str, Field(min_length=10, max_length=80, description="Código de verificación impreso en el certificado.")],
    ) -> Verificacion:
        """HU-05 · CA-05.1 y CA-05.2. Acceso público sin iniciar sesión. Muestra solo nombres, tipo de certificado y fecha de emisión; nunca calificaciones (E-03, R1)."""
        ...
