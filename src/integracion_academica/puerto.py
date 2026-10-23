"""Puerto hacia el sistema académico (ADR-002). Solo lectura (R2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SistemaAcademicoNoDisponible(Exception):
    """El sistema académico no respondió a tiempo (E-06)."""


@dataclass(frozen=True)
class DatosEstudiante:
    estudiante_id: int
    nombres: str


@dataclass(frozen=True)
class Calificacion:
    asignatura: str
    nota: float


class ProveedorDatosAcademicos(Protocol):
    def obtener_estudiante(self, estudiante_id: int) -> DatosEstudiante: ...

    def obtener_calificaciones(self, estudiante_id: int, tipo_certificado: str) -> list[Calificacion]: ...
