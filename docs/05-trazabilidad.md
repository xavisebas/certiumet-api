# 05 · Matriz de trazabilidad

**Proyecto:** CertiUMET API · **Hito:** H4 (`v0.4.0`) · **Fecha de corte:** 09/11/2026 (commit `b1a8b46`)

Esta matriz une cada requisito con el escenario de calidad que lo motiva, la decisión de arquitectura (ADR), el artefacto que lo implementa, el commit o pull request (PR) donde entró a `main` y el check del pipeline que lo verifica en cada cambio. Los identificadores son los mismos en todos los documentos: HU y CA en [`07`](07-historias-y-criterios.md), D, R y E en [`01`](01-contexto-y-drivers.md), ADR en [`03-adr/`](03-adr/README.md) y las operaciones en [`api/openapi.yaml`](../api/openapi.yaml).

## 1. Requisitos funcionales (historias de usuario)

| Requisito | Escenario | ADR | Artefacto | Commit / PR | Verificación en el pipeline |
|---|---|---|---|---|---|
| **HU-01** Pedir un certificado · CA-01.1, CA-01.2 | E-07 (D6, D4) | ADR-002, ADR-003 | `POST /api/v1/solicitudes` (`crearSolicitud`) · [`solicitudes/vistas.py`](../src/solicitudes/vistas.py) `SolicitudesVista` · [`casos_uso.py`](../src/solicitudes/casos_uso.py) `crear_solicitud` · [`hu01.feature`](../tests/features/hu01.feature) | `cdb2669` (H2) | `pruebas` (pytest) y prueba de humo HU-01 (201) · `contrato` (Spectral) |
| HU-01 · CA-01.3 Temporada alta | E-07 | ADR-001 | Escenario `@carga` en [`hu01.feature`](../tests/features/hu01.feature) | `cdb2669` | **No se ejecuta en el CI**: se excluye con `-m 'not carga'` (ver sección 4) |
| HU-01 · CA-01.4 Sistema académico sin respuesta | E-06 | ADR-002 | [`integracion_academica/puerto.py`](../src/integracion_academica/puerto.py) y [`adaptador_simulado.py`](../src/integracion_academica/adaptador_simulado.py) | `cdb2669` | `pruebas` |
| **HU-02** Consultar el estado · CA-02.1, CA-02.2 | E-01, E-04 (D1) | ADR-003 | `GET /api/v1/solicitudes/{id}` · `SolicitudDetalleVista` · `consultar_solicitud` · [`auditoria/adaptadores.py`](../src/auditoria/adaptadores.py) (bitácora) · [`hu02.feature`](../tests/features/hu02.feature) | `cdb2669` | `pruebas` y prueba de humo E-01 (401 sin token) y HU-02 (200) |
| **HU-03** Aprobar o rechazar · CA-03.1 a CA-03.4 | E-02, E-04 (D2, D1) | ADR-001, ADR-003 | `PATCH /api/v1/solicitudes/{id}/resolucion` · `ResolucionVista` · `resolver_solicitud` · [`hu03.feature`](../tests/features/hu03.feature) | `cdb2669` | `pruebas` (CA-03.2 con 1 000 pares de aprobaciones simultáneas sobre PostgreSQL 16) |
| HU-03 · CA-03.5 Rechazo sin motivo (422) | E-04 | ADR-003 | Paso nuevo en [`test_hu03_resolver_pedido.py`](../tests/test_hu03_resolver_pedido.py) | `ec2f6cc` · PR #9 (issue #3) | `pruebas` |
| HU-03 · CA-03.6 Sistema académico sin respuesta al aprobar (503) | E-06 (D3) | ADR-002 | `ServicioNoDisponible` en [`solicitudes/dominio.py`](../src/solicitudes/dominio.py) y [`config/errores.py`](../src/config/errores.py) · respuesta 503 en el contrato | `37711cc`, `d32cf80`, conflicto resuelto en `1af9e2a` · PR #10 (issue #4) | `pruebas` · `contrato` |
| **HU-04** Descargar el certificado · CA-04.1 a CA-04.3 | E-01, E-04 (D1) | ADR-003 | `GET /api/v1/solicitudes/{id}/certificado` · [`emision/vistas.py`](../src/emision/vistas.py) `CertificadoVista` · [`emision/pdf.py`](../src/emision/pdf.py) · [`hu04.feature`](../tests/features/hu04.feature) | `cdb2669` | `pruebas` |
| **HU-05** Verificar un certificado · CA-05.1, CA-05.2 | E-03 (D2) | ADR-003 | `GET /api/v1/verificaciones/{codigo}` · `VerificacionVista` · [`emision/dominio.py`](../src/emision/dominio.py) (firma del código) · [`hu05.feature`](../tests/features/hu05.feature) | `cdb2669` | `pruebas` y prueba de humo CA-05.2 (código alterado: `valido` en falso) |

## 2. Requisitos de calidad sin historia de usuario

| Requisito | Escenario | ADR | Artefacto | Commit / PR | Verificación en el pipeline |
|---|---|---|---|---|---|
| D3 · Cambiar el adaptador académico sin tocar el resto | E-05 | ADR-002, ADR-003 | [`.importlinter`](../.importlinter) (3 contratos de dependencia entre módulos) | `cdb2669` | `calidad` (import-linter) |
| D5 · Instalación sencilla y repetible | E-08 | ADR-005 | [`requirements.txt`](../requirements.txt), migraciones y [`ci.yml`](../.github/workflows/ci.yml) | `23b1d72` · PR #8; `b1a8b46` · PR #15 | `pruebas`: instala desde cero, aplica migraciones en una base vacía y levanta la API |
| R1 · Datos personales protegidos (LOPDP) | E-01 | ADR-003 | [`config/autenticacion.py`](../src/config/autenticacion.py) (JWT) · [`scripts/escanear_secretos.py`](../scripts/escanear_secretos.py) | `cdb2669`; PR #15 | `pruebas` (prueba de humo E-01) · `seguridad` (sin secretos versionados) |
| R4 · Software libre y dependencias sin vulnerabilidades conocidas | — | ADR-005 | [`requirements-dev.txt`](../requirements-dev.txt) | `f2c73c8` · PR #12 (issue #11) | `seguridad` (pip-audit) |
| R7 · Versionar en GitHub, listo para integración continua | E-08 | ADR-004 | [`CONTRIBUTING.md`](../CONTRIBUTING.md), regla `proteger-main`, etiquetas SemVer | PR #7 a #15 | Los 6 checks son obligatorios en `main` |
| Contrato como fuente de la API (T04, T05) | E-03, E-05 | ADR-005 | [`api/openapi.yaml`](../api/openapi.yaml) · [`.spectral.yaml`](../.spectral.yaml) | `cdb2669`; PR #10 | `contrato` (Spectral) · `documentacion` (Redocly) |
| Código sin patrones inseguros | E-01, E-02 | ADR-005 | Bandit sobre `src/` | PR #15 | `analisis-estatico` |
| Uso de IA registrado y verificado | — | — | [`04-registro-ia.md`](04-registro-ia.md) | Todos los hitos | Revisión en cada PR (plantilla, casilla "Uso de IA registrado") |

## 3. Decisiones (ADR) y dónde se aplican

| ADR | Decisión | Dónde se ve en el código o en el pipeline |
|---|---|---|
| [ADR-001](03-adr/ADR-001-base-de-datos-postgresql.md) | PostgreSQL | Servicio `postgres:16` del job `pruebas`; CA-03.2 (concurrencia) solo corre con PostgreSQL |
| [ADR-002](03-adr/ADR-002-integracion-sistema-academico.md) | Puerto y adaptador para el sistema académico | `integracion_academica/puerto.py`; CA-01.4 y CA-03.6 (503) |
| [ADR-003](03-adr/ADR-003-estilo-arquitectonico.md) | Monolito modular hexagonal | Módulos `solicitudes`, `emision`, `auditoria` e `integracion_academica`; job `calidad` (import-linter) |
| [ADR-004](03-adr/ADR-004-control-de-versiones-git.md) | Git con GitHub Flow | PR #7 a #15, regla `proteger-main`, etiquetas `v0.1.0` a `v0.4.0` |
| [ADR-005](03-adr/ADR-005-stack-de-construccion-y-pruebas.md) | Django REST Framework, pytest-bdd y cadena CASE | Jobs `pruebas`, `contrato` y `documentacion` |
| [ADR-006](03-adr/ADR-006-idioma-de-los-artefactos.md) | Lenguaje del negocio en español | Nombres de módulos, operaciones y criterios en español en todo el repositorio |

## 4. Auditoría de la trazabilidad (revisión del 09/11/2026)

| Pregunta | Resultado |
|---|---|
| ¿Hay requisitos sin prueba? | Sí, uno: **CA-01.3 (E-07, temporada alta)** tiene escenario, pero la prueba de carga se excluye del CI porque necesita varios minutos y un entorno con más recursos. Queda pendiente para un job programado (no en cada PR). |
| ¿Hay decisiones sin implementar? | No. Los seis ADR se ven en el código o en el pipeline (sección 3). |
| ¿Hay commits sin issue? | Sí, los de las semanas 1 y 2 (`baa4be7` a `bff63d0`), porque el flujo issue → rama → PR se adoptó en la semana 3 (ADR-004). Las historias HU-01 a HU-05 se implementaron en `cdb2669` directamente en `main`. Desde la semana 3, todos los cambios tienen issue y PR (issues #1 a #6, #11, #16 y #17). |
| ¿Hay PR integrados sin checks? | Solo el PR #7, porque el CI llegó en el PR #8. Desde el PR #9 los checks son obligatorios, y desde el PR #15 son 6. |
| ¿`main` acepta cambios sin checks obligatorios? | No. La regla `proteger-main` exige PR, los 6 checks y conversaciones resueltas; un `push` directo fue rechazado (GH013). |
| ¿Hay uso de IA sin registrar? | No. Cada hito tiene sus filas en `04-registro-ia.md` (filas 1 a 24). |

## 5. Cómo mantener esta matriz

- Cada issue nuevo nombra la historia, el criterio (CA-0n.m reservado antes de crear la rama) y el escenario.
- Cada PR enlaza su issue con `Closes #n` y marca en la plantilla si cambió un criterio, el contrato o un ADR.
- Al integrar, se agrega la fila o se actualiza la columna "Commit / PR" de esta matriz.
