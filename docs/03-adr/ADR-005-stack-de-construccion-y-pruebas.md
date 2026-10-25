# ADR-005 · Herramientas de construcción y pruebas del servicio

**Estado:** Aceptada
**Fecha:** 24/10/2026
**Escenarios relacionados:** E-01, E-02, E-03, E-04, E-05
**Drivers relacionados:** D1, D2, D3, D5
**Restricciones relacionadas:** R4, R5, R7

## Contexto

El ADR-003 fijó el estilo (monolito modular con arquitectura hexagonal en Django) y el ADR-001 la base de datos (PostgreSQL). En la semana 2 hubo que elegir con qué herramientas se construye y se prueba el servicio a partir del contrato `api/openapi.yaml`: framework de la API, generación del código base (tarea T06), framework de pruebas que use los criterios en Gherkin del `07` (tareas T01 y T07) y análisis estático (tarea T08). En la clase del 23/10/2026 se pidió registrar en un ADR el framework y las herramientas elegidas, y comparar tres alternativas para generar el código.

## Alternativas consideradas

| Decisión | Alternativa | A favor | En contra |
|---|---|---|---|
| Framework de la API | **Django REST Framework** | Ya fijado por el ADR-003; experiencia previa del estudiante con Django; soporte directo de PostgreSQL y `select_for_update` | OpenAPI Generator no tiene generador de servidor para Django |
| | FastAPI | OpenAPI Generator sí genera stubs para FastAPI | Obliga a cambiar el ADR-003 y los diagramas de la `v0.1.0`; el estudiante no lo maneja, lo que suma tiempo de aprendizaje (R5) |
| Generación del código base (T06) | OpenAPI Generator 7.26.0 | Genera las 5 operaciones y los esquemas del contrato, siempre igual | Solo para FastAPI; 70 hallazgos de ruff en el código generado; las operaciones quedan vacías |
| | datamodel-code-generator 0.86.0 | Genera las 9 clases de los esquemas sin hallazgos de ruff | Solo modelos Pydantic; no genera rutas ni lógica y no usa los serializadores de DRF |
| | **Claude Opus 5.5 (IA), con verificación** | Generó el esqueleto completo en Django con puertos, adaptadores y lógica de las 5 operaciones | La primera versión tuvo defectos (3 hallazgos de ruff y 13 de 14 pruebas fallando); la respuesta cambia entre ejecuciones |
| Pruebas desde los criterios | **pytest 8.4 + pytest-bdd 8.1** | Lee los mismos `.feature` del `07` con `# language: es`; se integra con pytest-django y PostgreSQL | Un paso Gherkin mal escrito no se detecta hasta ejecutar |
| | behave | También lee Gherkin en español | Integración con Django menos directa; no reutiliza las fixtures de pytest |
| Análisis estático | **ruff 0.14 + import-linter 2.15** | ruff es un solo comando rápido; import-linter controla las reglas de módulos del ADR-003 | Dos herramientas en lugar de una |
| | flake8 + isort | Muy conocidas | Más lentas y más archivos de configuración; no controlan dependencias entre módulos |

## Decisión

- **API:** Django 5.2 y Django REST Framework 3.16, con Python 3.10 o superior (probado en 3.10 y 3.13).
- **Código base:** el esqueleto en Django se genera con IA (Claude) y **nunca se acepta sin pasar por la cadena**: ruff, import-linter y las pruebas de los criterios sobre PostgreSQL. OpenAPI Generator se mantiene para la documentación HTML y como stubs de referencia del contrato; datamodel-code-generator queda como opción para modelos tipados si más adelante se necesitan. La comparación con pesos está en el `08-informe-cadena-case.md`, sección 5.
- **Pruebas:** pytest + pytest-bdd + pytest-django. Los `.feature` se generan desde el `07` con `scripts/extraer_features.py`, para que criterio y prueba tengan el mismo texto.
- **Análisis estático:** ruff y import-linter, con las reglas en `pyproject.toml` y `.importlinter`.
- **Concurrencia (E-02):** se mantienen las dos barreras del ADR-001: bloqueo por fila al resolver y `UNIQUE` sobre `solicitud_id` en el certificado. La prueba de mutación del 22/10 mostró que, sin el bloqueo, `UNIQUE` evita el duplicado pero la API responde 500 en lugar de 409.

## Consecuencias

**Positivas**

- No se modifica nada de la `v0.1.0` (ADR-003 y vistas C4 siguen válidos).
- El código generado con IA queda controlado por herramientas que dan el mismo resultado cada vez.
- Toda la cadena corre con un comando (`bash scripts/cadena.sh`) y queda lista para GitHub Actions en la semana 3.

**Negativas y riesgos**

- No hay generación automática de rutas Django desde el contrato; si el contrato cambia, la API se ajusta a mano o con IA, y solo las pruebas detectan la diferencia.
- Depender de la IA para el esqueleto exige revisar cada salida; el registro de esa revisión está en el `04`.

## Vínculos

| Tipo | Elemento |
|---|---|
| Decisiones | ADR-001 (PostgreSQL, `UNIQUE` y bloqueo), ADR-003 (estilo), ADR-004 (idioma) |
| Tareas del mapa | T01, T06, T07, T08 (`06-mapa-toolchain.md`) |
| Evidencia | `docs/evidencias/04-stubs.txt`, `05-ruff.txt`, `06-import-linter.txt`, `07-pruebas.txt`, `11-matriz-generacion.txt` |

## Referencias

ISO/IEC. (2008). *ISO/IEC 14102:2008 Information technology — Guideline for the evaluation and selection of CASE tools*. International Organization for Standardization.

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
