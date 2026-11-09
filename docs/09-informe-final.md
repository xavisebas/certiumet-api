# 09 · Informe final del proyecto integrador

**Proyecto:** CertiUMET API · **Módulo:** M8 Automatización de Procesos de Software · **Versión:** `v0.4.0` (hito H4)
**Integrante:** Xavier Guaygua (trabajo individual) · **Fecha:** 09/11/2026

Este informe no copia los artefactos: los resume y enlaza. Cada sección indica dónde está la evidencia en el repositorio.

> **Nota de numeración:** el informe usa el número 09, como pide la rúbrica de la semana 4, y convive con [`09-revision-de-codigo.md`](09-revision-de-codigo.md), que es de la semana 2. Lo mismo pasa con los dos documentos 08.

## (a) Resumen del caso y alcance

La Secretaría General de la UMET entrega certificados académicos en ventanilla o por correo. El estudiante no sabe en qué va su pedido, las calificaciones circulan sin control de acceso y un tercero no puede comprobar si un certificado es auténtico. CertiUMET es una API REST que permite pedir, consultar, aprobar o rechazar, descargar en PDF y verificar certificados, y que registra cada acceso a datos personales en una bitácora ([README](../README.md), [`01-contexto-y-drivers.md`](01-contexto-y-drivers.md)).

**Alcance del módulo:** cinco historias de usuario (HU-01 a HU-05), cinco endpoints, un sistema académico simulado y datos ficticios. Quedan **fuera**: el sistema académico real (Oracle), el envío de correos, la interfaz web y el despliegue en producción.

| Hito | Contenido | Etiqueta |
|---|---|---|
| H1 | Dossier de arquitectura | `v0.1.0` |
| H2 | Cadena CASE: historias, contrato, esqueleto y pruebas | `v0.2.0` |
| H3 | Repositorio gobernado: GitHub Flow, CI, `main` protegida, conflicto documentado | `v0.3.0` |
| H4 | Pipeline con seis quality gates, trazabilidad e informe final | `v0.4.0` |

## (b) Arquitectura: drivers, escenarios y decisiones

- **Drivers** ([`01`](01-contexto-y-drivers.md)): D1 proteger las calificaciones, D2 certificados únicos y comprobables, D3 conexión al sistema académico cambiable y sin afectarlo, D4 picos de pedidos, D5 despliegue sencillo y D6 funcionalidad básica.
- **Escenarios de calidad prioritarios:** E-01 confidencialidad y E-02 integridad (prioridad 1), E-03 autenticidad, E-04 responsabilidad y E-05 modificabilidad (prioridad 2).
- **Vistas C4** como código: [`02-vistas-c4/`](02-vistas-c4/README.md).
- **Decisiones** ([`03-adr/`](03-adr/README.md)):

| ADR | Decisión | Escenarios |
|---|---|---|
| [ADR-001](03-adr/ADR-001-base-de-datos-postgresql.md) | PostgreSQL, por transacciones y bloqueo de filas | E-02 |
| [ADR-002](03-adr/ADR-002-integracion-sistema-academico.md) | Sistema académico detrás de un puerto y un adaptador, solo lectura | E-05, E-06, E-01 |
| [ADR-003](03-adr/ADR-003-estilo-arquitectonico.md) | Monolito modular con arquitectura hexagonal (elegido con la [matriz ponderada](03-adr/matriz-decision.md)) | E-01 a E-05 |
| [ADR-004](03-adr/ADR-004-control-de-versiones-git.md) | Git con GitHub Flow (comparado con SVN en [`08-matriz-git-vs-svn.md`](08-matriz-git-vs-svn.md)) | E-08 |
| [ADR-005](03-adr/ADR-005-stack-de-construccion-y-pruebas.md) | Django REST Framework, pytest-bdd y cadena CASE | E-02, E-05 |
| [ADR-006](03-adr/ADR-006-idioma-de-los-artefactos.md) | Lenguaje del negocio en español | E-05 |

## (c) Proceso, toolchain y herramientas CASE

El proceso por fases, las diez tareas puntuadas por frecuencia × esfuerzo × riesgo y la herramienta elegida para cada tarea están en [`06-mapa-toolchain.md`](06-mapa-toolchain.md). La evaluación de las herramientas y de la generación de código está en [`08-informe-cadena-case.md`](08-informe-cadena-case.md).

| Fase | Herramienta | Tarea | Dónde corre |
|---|---|---|---|
| Analizar | Gherkin y `scripts/extraer_features.py` | T01, T02: criterios en el 07 = archivos `.feature` | Job `calidad` |
| Diseñar | Mermaid (C4), OpenAPI 3.0.3 y Spectral 6.17.1 | T03, T04 | Job `contrato` |
| Diseñar | Prism (mock) y Redocly (documentación HTML) | T05: documentación y servidor mock | Job `documentacion` (Redocly); Prism en local |
| Construir | OpenAPI Generator y datamodel-code-generator | T06: código base desde el contrato | Local (`scripts/cadena.sh`) |
| Probar | pytest-bdd sobre PostgreSQL 16 | T07: pruebas de aceptación y concurrencia (E-02) | Job `pruebas` |
| Probar | ruff, import-linter y Bandit | T08: lint, reglas de dependencia y análisis estático | Jobs `calidad` y `analisis-estatico` |
| Integrar | GitHub, pull requests y GitHub Actions | T09: revisión y pipeline | Regla `proteger-main` |
| Asegurar | Script de secretos y pip-audit | Seguridad de la cadena de suministro | Job `seguridad` |

## (d) Versionamiento y gobierno del repositorio

- **Flujo:** GitHub Flow (issue → rama corta → PR con `Closes #n` → CI → revisión → merge), definido en el [ADR-004](03-adr/ADR-004-control-de-versiones-git.md) y en [`CONTRIBUTING.md`](../CONTRIBUTING.md).
- **Commits:** Conventional Commits 1.0.0. **Versiones:** SemVer 2.0.0, con una etiqueta anotada por hito (`v0.1.0` a `v0.4.0`).
- **Protección de `main`:** regla `proteger-main` con PR obligatorio, 6 checks obligatorios, conversaciones resueltas y sin `force push` ni borrado. Un `push` directo fue rechazado con el error GH013 ([`11-revision-seguridad.md`](11-revision-seguridad.md)).
- **Conflicto deliberado** entre los PR #9 y #10, documentado en [`10-reporte-conflicto.md`](10-reporte-conflicto.md).
- **Dependencias:** pip-audit encontró 7 vulnerabilidades; se corrigieron en el PR #12.
- **Proyecto individual:** la revisión cruzada se reemplazó por autorrevisión escrita en cada PR ([`CONTRIBUTING.md`](../CONTRIBUTING.md), sección 4).
- **Trazabilidad** de punta a punta: [`05-trazabilidad.md`](05-trazabilidad.md).

## (e) Pipeline de integración continua

Archivo: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). Corre en cada PR hacia `main` y en cada `push` a `main`. Cada job es una puerta de calidad y un check obligatorio de `main`:

| Puerta | Qué verifica | Escenario o tarea |
|---|---|---|
| `calidad` | ruff, import-linter y criterios del 07 = `.feature` | T01, T08, E-05 |
| `pruebas` (depende de `calidad`) | Escenarios pytest-bdd de HU-01 a HU-05 sobre PostgreSQL 16 (incluye los 1 000 pares de E-02), migraciones en una base vacía y **prueba de humo** con la API levantada ([`scripts/prueba_humo.py`](../scripts/prueba_humo.py)) | T07, E-01, E-02, E-03, E-08 |
| `analisis-estatico` | Bandit sobre `src/` (severidad y confianza media o alta) | E-01, E-02 |
| `contrato` | Spectral sobre `api/openapi.yaml`; falla también con advertencias | T04 |
| `documentacion` (depende de `contrato`) | Redocly genera `docs/api/index.html` y lo publica como artefacto | T05 |
| `seguridad` | [`scripts/escanear_secretos.py`](../scripts/escanear_secretos.py) y pip-audit | R1, R4 |

**Buenas prácticas:**
- permisos mínimos (`contents: read`);
- acciones y herramientas con versión exacta (`actions/checkout@v4.4.0`, Spectral 6.17.1, Redocly 2.76.0);
- sin secretos;
- tiempo máximo por job;
- `concurrency` para cancelar ejecuciones viejas.

**Falla detectada y corregida (PR #15):** en la primera ejecución, la puerta `calidad` falló porque `scripts/metricas_dora.py` tenía una línea de 127 caracteres, por encima del límite de 120 del proyecto (ruff E501). Como `pruebas` depende de `calidad`, no llegó a ejecutarse. Se corrigió con el commit `7168a82` (`fix(ci): corrige la falla de lint detectada por la puerta calidad (E501)`) y los 6 checks quedaron en verde. Evidencias: [`docs/evidencias/semana4/`](evidencias/semana4/README.md).

**Esqueleto ejecutable:** en el job `pruebas`, la API se instala desde cero, aplica sus migraciones en una base PostgreSQL vacía y se levanta. Después, la prueba de humo recorre el caso principal:
- sin token, la API responde 401 (E-01);
- un estudiante pide un certificado (201, HU-01);
- lo consulta (200, HU-02);
- un código alterado se marca como no válido (CA-05.2).

El caso de este proyecto equivale al caso "reservar cita" de la consigna: HU-01, con el escenario prioritario E-01.

## (f) Métricas aproximadas tipo DORA

Se calcularon con [`scripts/metricas_dora.py`](../scripts/metricas_dora.py) sobre el historial de `main` hasta el commit `b1a8b46` (PR #15). La salida completa está en [`docs/evidencias/semana4/metricas-dora.md`](evidencias/semana4/metricas-dora.md). Como el proyecto no despliega a producción, **cada merge de un PR en `main` cuenta como un despliegue**, y cada etiqueta, como una entrega.

| Métrica | Valor | Cómo se calculó |
|---|---|---|
| Frecuencia de integración | 5,2 PR por semana (8 PR en 1,5 semanas) | Merges de PR en `main` desde el primer PR (29/10) |
| Frecuencia de entrega | 0,9 versiones por semana (3 en 3,5 semanas) | Etiquetas `vX.Y.Z` desde el primer commit |
| Tiempo de entrega de cambios | mediana 0,5 h (mín, 0,1 h, máx, 0,7 h) | Primer commit de la rama → merge en `main` |
| Tasa de fallos de cambios | 12 % (1 de 8 PR) | PR que tuvieron una falla del pipeline antes del merge |
| Tiempo de recuperación | 13 min | Commit que rompió el pipeline → commit que lo corrigió |
| Tasa de retrabajo | 25 % (2 de 8 PR) | PR con commits de tipo `fix` |

**Lectura de los resultados:**
- Los valores parecen de un equipo de "alto desempeño" (Forsgren et al., 2018), pero esa conclusión no es válida aquí.
  - Es una sola persona, con cambios pequeños hechos y revisados en la misma sesión. Por eso el tiempo de entrega mide horas de trabajo seguido, no la espera de un revisor.
  - Son solo 8 PR, así que un fallo más cambia mucho la tasa.
- La tasa de fallos solo cuenta las fallas del pipeline **antes** del merge. Como `main` está protegida, ninguna falla llegó a `main`. En un equipo con despliegue real, esta métrica se mediría sobre fallas en producción.
- Las semanas 1 y 2 no usaron PR. Por eso la frecuencia se mide desde el 29/10 y no desde el inicio del módulo.
- Lo que sí muestran las métricas es una tendencia: cambios pequeños, integración frecuente y una falla corregida en minutos gracias a una puerta automática. Es el comportamiento que el flujo buscaba (ADR-004).

## (g) Análisis crítico de decisiones y herramientas

**Lo que funcionó:**
- **Contrato primero con Spectral en el CI.** El contrato fue la fuente de la documentación, del mock y del código base. Validarlo en cada PR evitó que un error del contrato pasara al código (T04 era la tarea de mayor riesgo junto con T07).
- **Pruebas derivadas de los criterios.** `extraer_features.py --check` obliga a que los criterios del 07 y las pruebas sean los mismos. El conflicto de los PR #9 y #10 se detectó justo ahí.
- **Puertas separadas.** Con un solo job (semana 3), una falla no decía qué se rompió. Con seis jobs, el PR muestra de inmediato la puerta que falló (por ejemplo, `calidad` en el PR #15).
- **Actualizar dependencias pasando por las pruebas.** Al subir pytest a 9.2, las 16 pruebas fallaron por una incompatibilidad con pytest-bdd 8.1. Se detectó antes de integrar y se corrigió en el PR #12.

**Lo que fue pesado o no aportó lo esperado:**
- **El código base generado (T06).** OpenAPI Generator no tiene un generador de servidor para Django, así que se generaron 24 archivos con `python-fastapi` solo como referencia. El esqueleto en Django se generó con IA siguiendo esa referencia ([`08`](08-informe-cadena-case.md), sección 3). Mantener esos stubs sincronizados no aportó, y por eso dejaron de versionarse (PR #7). Con un framework que genera el contrato desde el código, como FastAPI, este paso sobraría; aquí se mantuvo el contrato primero porque Spectral y las pruebas dependen de él.
- **El servidor mock con Prism (T05).** Sirvió para revisar el contrato en la semana 2, pero cuando el esqueleto ya respondía, la prueba de humo contra la API real dio más confianza que el mock.
- **Métricas DORA con un solo integrante.** El cálculo es útil para practicar, pero los números no permiten comparar con otros equipos.

**Lo que haría distinto:**
- Usar el flujo con PR desde la semana 1. Así las historias HU-01 a HU-05 también tendrían issue y PR, en lugar de un solo commit grande (`cdb2669`).
- Ejecutar la prueba de carga de E-07 en un job programado.
- Agregar análisis estático más profundo (CodeQL) y un despliegue continuo a un entorno de pruebas (por ejemplo, Render con health check), que en este módulo quedó como opcional.

**Riesgos que siguen abiertos:**
- No hay revisión de otra persona.
- El sistema académico es simulado.
- La clave de desarrollo del JWT tiene un valor por defecto que en producción debe reemplazarse por una variable de entorno (supuesto A2 del 01).

## (h) Uso de IA y verificación

El registro completo está en [`04-registro-ia.md`](04-registro-ia.md) (filas 1 a 24): herramienta y versión, qué se pidió, qué produjo, qué defectos se encontraron, qué se aceptó, modificó o rechazó, y cómo se verificó.

- **Herramienta:** Claude Opus 5.5 (web).
- **Usos:**
  - borradores de documentos, como los ADR, las historias y este informe;
  - el esqueleto de código y los scripts;
  - el workflow del CI;
  - la explicación de errores.
- **Reglas que se siguieron:**
  - la IA es una herramienta y no la autora;
  - no se ingresaron credenciales ni datos personales; el token de GitHub nunca se compartió;
  - se hizo un commit antes de cada instrucción a la IA para ver qué cambió;
  - cada salida se verificó con una herramienta, no solo leyéndola.
- **Errores reales de la IA que detectó la cadena de herramientas:**
  - el rango de versiones de pytest que propuso rompió las pruebas (PR #12);
  - la línea demasiado larga en el script de métricas la detectó la puerta `calidad` (PR #15);
  - el número del ADR de Git chocaba con el de idioma (semana 3).
- **Revisión del workflow** con una lista de verificación: permisos mínimos, versiones fijas, sin secretos, `timeout` por job, dependencias entre jobs y checks obligatorios. Está registrada en la fila 22 del 04 y en la autorrevisión del PR #15.

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The science of lean software and DevOps*. IT Revolution Press.

Humble, J., & Farley, D. (2010). *Continuous delivery: Reliable software releases through build, test, and deployment automation*. Addison-Wesley.

Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1* (NIST SP 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
