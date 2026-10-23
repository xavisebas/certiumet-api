"""Elige el adaptador del sistema académico con una variable de entorno (ADR-002)."""

from django.conf import settings

from integracion_academica.adaptador_simulado import AdaptadorAcademicoSimulado
from integracion_academica.puerto import ProveedorDatosAcademicos


def crear_proveedor() -> ProveedorDatosAcademicos:
    if settings.ADAPTADOR_ACADEMICO == "simulado":
        return AdaptadorAcademicoSimulado()
    raise NotImplementedError(f"Adaptador académico no disponible: {settings.ADAPTADOR_ACADEMICO}")
