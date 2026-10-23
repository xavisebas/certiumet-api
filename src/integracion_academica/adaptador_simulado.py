"""Adaptador simulado del sistema académico con datos ficticios (supuesto A1).

En el esqueleto responde en memoria. El AdaptadorAcademicoOracle de ADR-002 queda
como extensión posterior y debe cumplir el mismo puerto.
"""

from __future__ import annotations

from integracion_academica.puerto import Calificacion, DatosEstudiante, SistemaAcademicoNoDisponible

NOMBRES_FICTICIOS = ("Ana Pérez", "Luis Andrade", "María Torres", "Jorge Cevallos", "Sofía Ruiz")


class AdaptadorAcademicoSimulado:
    def __init__(self, disponible: bool = True) -> None:
        self.disponible = disponible

    def _comprobar(self) -> None:
        if not self.disponible:
            raise SistemaAcademicoNoDisponible("El sistema académico simulado no responde.")

    def obtener_estudiante(self, estudiante_id: int) -> DatosEstudiante:
        self._comprobar()
        return DatosEstudiante(estudiante_id, NOMBRES_FICTICIOS[estudiante_id % len(NOMBRES_FICTICIOS)])

    def obtener_calificaciones(self, estudiante_id: int, tipo_certificado: str) -> list[Calificacion]:
        self._comprobar()
        return [Calificacion("Ingeniería de requisitos", 9.0), Calificacion("Arquitectura de software", 8.5)]
