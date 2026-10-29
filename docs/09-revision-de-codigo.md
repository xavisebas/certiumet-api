# 09 · Revisión del código con rúbrica

**Proyecto:** CertiUMET API · **Semana:** 2 · **Fecha:** 24/10/2026 · **Versión revisada:** `v0.2.0`
**Revisor:** Xavier Guaygua · **Documentos relacionados:** `07-historias-y-criterios.md`, `api/openapi.yaml`, `ADR-005`, `docs/evidencias/`

La práctica de la clase del 23/10/2026 pide revisar el código en parejas con una rúbrica (tarea T09 del mapa). Como el proyecto es individual (R5), la revisión la hace el estudiante apoyado en la evidencia de las herramientas de la cadena; queda pendiente que un compañero del módulo la repita con la misma tabla, igual que la revisión cruzada de las vistas C4.

**Escala:** Cumple · Cumple con observación · No cumple.

| Criterio | Qué se revisó | Evidencia | Resultado | Hallazgo o acción |
|---|---|---|---|---|
| Correctitud frente a los criterios | Que cada CA del `07` tenga una prueba y que pase | 14 de 14 pruebas pasan sobre PostgreSQL; CA-01.3 (`@carga`) excluida a propósito (`07-pruebas.txt`) | Cumple con observación | El rechazo sin motivo respondía 422 en el código, pero no tenía un CA ni una prueba. **Resuelto el 29/10/2026:** CA-03.5 y su prueba (issue #3) |
| Concurrencia (E-02) | Que dos aprobaciones simultáneas no emitan dos certificados | CA-03.2: 1 000 pares, 0 duplicados, 409 en 1 000/1 000; prueba de mutación sin bloqueo: la prueba falla | Cumple | — |
| Conformidad con el contrato | Que rutas, métodos, códigos y cuerpos coincidan con `openapi.yaml` | Rutas de `config/urls.py` iguales a los 5 paths; las pruebas comprueban 200, 201, 403, 404, 409 y 422 y el esquema `Error` | Cumple con observación | Si el sistema académico no respondía **al aprobar**, la emisión fallaba con 500, que no estaba en el contrato. **Resuelto el 29/10/2026:** responde 503 con `Retry-After`, está en el contrato y lo verifica una prueba (issue #4) |
| Seguridad y datos personales (R1, E-01, E-03) | Control por dueño, datos mínimos en la verificación, sin cédula | CA-02.2 y CA-04.3 (404 sin revelar si existe); CA-05.1 y CA-05.2 (solo nombres, tipo y fecha); `Verificacion` con `additionalProperties: false` | Cumple con observación | Las claves de JWT y de firma tienen valores por defecto solo para desarrollo en `settings.py`; en un despliegue real deben venir siempre de variables de entorno. Se agregará una comprobación al iniciar con `DEBUG=0` |
| Bitácora (E-04) | Que cada operación quede registrada con sus cinco campos y no se pueda editar | CA-02.2, CA-03.1 y CA-04.1 comprueban los cinco campos; el modelo bloquea `save` sobre registros existentes y `delete` | Cumple | — |
| Mantenibilidad (ADR-003, E-05) | Límites entre módulos y estilo del código | import-linter: 3 contratos cumplidos; ruff: 0 hallazgos (`05-ruff.txt`, `06-import-linter.txt`) | Cumple | — |
| Desempeño (E-07) | 95 % de respuestas en menos de 2 s con 500 pedidos en 10 min | No medido todavía | No cumple (pendiente) | Prueba de carga de CA-01.3 en la semana 3 |
| Código generado con IA | Que nada generado con IA entre sin verificar | Filas 12 a 14 del `04`: defectos encontrados por ruff y por las pruebas, y corregidos | Cumple | — |

## Resumen

- 5 criterios cumplen, 3 cumplen con observación y 1 queda pendiente (desempeño).
- Los dos hallazgos nuevos de esta revisión (500 cuando el sistema académico no responde al aprobar, y claves por defecto en la configuración) no los detectó ninguna herramienta de la cadena: salieron de leer el código contra el contrato y contra R1. Esto confirma lo que mostró la matriz del `08`: las herramientas revisan la forma, y la revisión humana sigue siendo necesaria para el significado.
