# CertiUMET API

[![CI](https://github.com/xavisebas/certiumet-api/actions/workflows/ci.yml/badge.svg)](https://github.com/xavisebas/certiumet-api/actions/workflows/ci.yml)

API REST para pedir, aprobar, emitir y verificar certificados académicos en la Secretaría General de la Universidad Metropolitana del Ecuador (UMET). El caso es académico: el sistema académico de la universidad se simula y todos los datos son ficticios.

## Datos del proyecto

| | |
|---|---|
| **Universidad** | Universidad Politécnica Estatal del Carchi (UPEC) · Posgrado |
| **Programa** | Maestría en Ingeniería de Software |
| **Módulo** | M8 · Automatización de Procesos de Software |
| **Docente** | Dr. José Luis Rodríguez Chinchilla |
| **Integrante** | Xavier Guaygua |
| **Modalidad** | Trabajo individual |
| **Versión actual** | `v0.2.0` · Hito H2: cadena CASE (contrato, esqueleto y pruebas) |

## Visión del proyecto

Hoy el trámite de certificados se hace en ventanilla o por correo: el estudiante no sabe en qué va su pedido, las calificaciones circulan sin control de acceso y nadie puede comprobar si un certificado es auténtico. CertiUMET permite:

- Registrar un pedido de certificado y consultar su estado.
- Aprobar o rechazar el pedido y emitir el certificado una sola vez.
- Descargar el certificado en PDF.
- Verificar la autenticidad de un certificado con su código.
- Registrar cada acceso a datos personales en una bitácora.

## Tecnología prevista

Python 3.12 (el esqueleto también se probó con 3.10) · Django REST Framework · PostgreSQL 16 · GitHub Actions (CI desde el hito H3) · Docker Compose (hito H4).

## Estructura del repositorio

```
api/openapi.yaml                  Contrato OpenAPI 3.0.3 (5 endpoints)
api/pruebas/                      Contrato con defectos sembrados para comparar linters
api/stubs/                        Código base generado con OpenAPI Generator
src/                              Esqueleto Django: solicitudes, emision, auditoria, integracion_academica
tests/                            Pruebas pytest-bdd generadas desde los criterios del 07
scripts/cadena.sh                 Ejecuta la cadena CASE y guarda la evidencia en docs/evidencias/
.spectral.yaml · .importlinter    Reglas de Spectral e import-linter
.github/workflows/ci.yml          Integración continua (job "pruebas", check obligatorio de main)
.github/ISSUE_TEMPLATE/           Plantillas de historia de usuario y de tarea técnica
.github/pull_request_template.md  Plantilla de pull request
CONTRIBUTING.md                   Ramas, commits, pull requests y versiones
```

## Cómo ejecutar la cadena

Requisitos: Python 3.10 o superior, Node.js 18 o superior, Java 11 o superior y PostgreSQL 16.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
npm install -g @stoplight/spectral-cli @stoplight/prism-cli @openapitools/openapi-generator-cli @redocly/cli
export POSTGRES_DB=certiumet POSTGRES_USER=certiumet POSTGRES_PASSWORD=<clave local> POSTGRES_HOST=localhost
bash scripts/cadena.sh
```

Sin las variables `POSTGRES_*` las pruebas usan SQLite y se omite la prueba de concurrencia de E-02, que necesita PostgreSQL (ADR-001).

Para levantar la API en local (con las mismas variables `POSTGRES_*`):

```bash
cd src
python manage.py migrate
python manage.py runserver
```

La API queda en `http://localhost:8000/api/v1/`. Los endpoints y sus respuestas están en `api/openapi.yaml`; la documentación HTML se genera en `docs/api/` con `scripts/cadena.sh`.

## Cómo contribuir

El repositorio usa **GitHub Flow** (ADR-004): todo cambio nace en un issue, se trabaja en una rama corta, entra a `main` por pull request con el CI en verde y revisión, y cada hito se etiqueta con SemVer. Las reglas completas están en [`CONTRIBUTING.md`](CONTRIBUTING.md).

> **Nota para el docente:** el proyecto es individual (clases seguidas en diferido por motivos de trabajo). La revisión cruzada de cada pull request se reemplaza por una autorrevisión escrita del autor, como se explica en `CONTRIBUTING.md`, sección 4.

## Estructura de la documentación

```
docs/
├── 01-contexto-y-drivers.md      Stakeholders, restricciones, drivers y escenarios de calidad
├── 02-vistas-c4/                 Vistas C4 como código (Mermaid)
│   ├── README.md                 Índice y revisión cruzada
│   ├── nivel-1-contexto.md
│   └── nivel-2-contenedores.md
├── 03-adr/                       Decisiones de arquitectura
│   ├── README.md                 Índice de ADR
│   ├── ADR-001-base-de-datos-postgresql.md
│   ├── ADR-002-integracion-sistema-academico.md
│   ├── ADR-003-estilo-arquitectonico.md
│   ├── ADR-004-idioma-de-los-artefactos.md
│   ├── ADR-005-stack-de-construccion-y-pruebas.md
│   └── matriz-decision.md        Matriz ponderada del estilo
├── 04-registro-ia.md             Registro de uso de IA
├── 06-mapa-toolchain.md          Proceso por fases, tareas F×E×R, herramientas CASE y evidencia
├── 07-historias-y-criterios.md   Historias de usuario y criterios en Gherkin
├── 08-informe-cadena-case.md     Informe final y matrices de selección de herramientas
├── 09-revision-de-codigo.md      Revisión del código con rúbrica
├── api/                          Documentación HTML generada desde el contrato
└── evidencias/                   Salidas de cada herramienta de la cadena
```

## Resumen de la arquitectura

- **Estilo:** monolito modular con arquitectura hexagonal ([ADR-003](docs/03-adr/ADR-003-estilo-arquitectonico.md)).
- **Base de datos:** PostgreSQL ([ADR-001](docs/03-adr/ADR-001-base-de-datos-postgresql.md)).
- **Sistema académico:** se consulta solo en lectura, a través de un puerto y un adaptador que se puede cambiar ([ADR-002](docs/03-adr/ADR-002-integracion-sistema-academico.md)).
- **Idioma:** lenguaje del negocio en español en el contrato, los criterios y el código del dominio ([ADR-004](docs/03-adr/ADR-004-idioma-de-los-artefactos.md)).

## Hitos del módulo

| Hito | Contenido | Etiqueta |
|---|---|---|
| H1 | Dossier de arquitectura | `v0.1.0` |
| H2 | Cadena CASE: historias, contrato, esqueleto y pruebas | `v0.2.0` |
| H3 | Ramas e implementación de la API | Pendiente |
| H4 | Pipeline de integración y despliegue continuo | Pendiente |
