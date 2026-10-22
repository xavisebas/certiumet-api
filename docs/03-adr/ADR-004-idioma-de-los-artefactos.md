# ADR-004 · Idioma de los artefactos de diseño y del código

**Estado:** Aceptada
**Fecha:** 22/10/2026
**Escenarios relacionados:** E-05
**Drivers relacionados:** D5, D6
**Restricciones relacionadas:** R5, R7

## Contexto

En la clase del 21/10/2026 se recomendó definir el idioma estándar del diseño desde las primeras fases. Las buenas prácticas sugieren el inglés porque es más universal y suele ser más corto. Sin embargo, el proyecto ya tiene una versión entregada (`v0.1.0`) donde los endpoints (`/api/v1/solicitudes`, `/api/v1/verificaciones/{codigo}`), los módulos (`solicitudes`, `emision`, `auditoria`, `integracion_academica`), el puerto `ProveedorDatosAcademicos` (ADR-002) y los estados del pedido (`EN_VALIDACION`) están en español. Los usuarios del sistema (S1, S2, S3 y S5) trabajan en español y los documentos del dossier se escriben en español.

Si se mezclan los idiomas sin una regla, un mismo concepto puede tener dos nombres (por ejemplo, "solicitud" en el contrato y `request` en el código), lo que vuelve ambiguo el requisito, algo que ISO/IEC/IEEE 29148 pide evitar, y rompe la trazabilidad entre la historia, el contrato y la prueba.

## Alternativas consideradas

| Alternativa | A favor | En contra |
|---|---|---|
| **Todo en inglés** (contrato, criterios y código) | Más universal; sigue la recomendación general | Obliga a cambiar endpoints, ADR y diagramas de la `v0.1.0`; aparece una tabla de traducción entre lo que dice la Secretaría y lo que dice el código |
| **Sin regla** (cada archivo en el idioma que salga) | No exige trabajo extra | Un concepto con dos nombres; búsquedas y trazabilidad más difíciles |
| **Lenguaje del negocio en español y términos técnicos del framework en inglés** | Un solo nombre por concepto, igual en la historia, el contrato, el código y la prueba; no rompe la `v0.1.0` | El código mezcla palabras en español con las palabras reservadas y librerías en inglés |

## Decisión

Se usa el **lenguaje del negocio en español** en todos los artefactos, como un lenguaje común entre usuarios y desarrollador (Evans, 2003):

- Documentos del dossier, historias y criterios en Gherkin (con la cabecera `# language: es`).
- Contrato OpenAPI: rutas, `operationId`, esquemas, campos JSON y mensajes de error (por ejemplo, `crearSolicitud`, `Solicitud`, `codigoVerificacion`).
- Código del dominio y de los casos de uso: módulos, clases, funciones y variables que nombran conceptos del negocio (por ejemplo, `Solicitud`, `resolver_solicitud`, `ProveedorDatosAcademicos`).

Se mantiene en **inglés** lo que imponen el lenguaje y las herramientas: palabras reservadas de Python, nombres propios de Django y de Django REST Framework (`settings.py`, `urls.py`, `serializers`), los decoradores `given`, `when` y `then` de pytest-bdd, y los mensajes de commit según Conventional Commits (`feat:`, `docs:`), cuyo texto se escribe en español.

Los nombres en código no llevan tildes ni eñes (`emision`, `codigo`), para evitar problemas de codificación en las herramientas.

## Consecuencias

**Positivas**

- Cada concepto tiene un solo nombre desde la historia hasta la prueba, lo que facilita la trazabilidad (T02) y las búsquedas en el repositorio.
- No se modifica nada de la `v0.1.0`.
- Los criterios en Gherkin los puede leer la Secretaría sin traducción.

**Negativas y riesgos**

- Si el proyecto se abre a un equipo que no habla español, habría que traducir el contrato y el dominio.
- Algunas herramientas generan nombres en inglés (por ejemplo, el código base de OpenAPI Generator); esos nombres se ajustan al adaptar los stubs.

## Vínculos

| Tipo | Elemento |
|---|---|
| Drivers | D5 (mantener el proyecto sencillo para un equipo de una persona), D6 (funcionalidad que entienden los usuarios) |
| Escenarios | E-05 (el contrato no cambia de forma al cambiar el adaptador) |
| Restricciones | R5 (una sola persona, cuatro semanas), R7 (versionado en GitHub) |
| Artefactos | `07-historias-y-criterios.md`, `api/openapi.yaml`, `src/` y `tests/` |

## Referencias

Evans, E. (2003). *Domain-driven design: Tackling complexity in the heart of software*. Addison-Wesley.

ISO/IEC/IEEE. (2018). *ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering*. International Organization for Standardization.

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
