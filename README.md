# CertiUMET API

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
| **Versión actual** | `v0.1.0` · Hito H1: dossier de arquitectura |

## Problema que resuelve

Hoy el trámite de certificados se hace en ventanilla o por correo: el estudiante no sabe en qué va su pedido, las calificaciones circulan sin control de acceso y nadie puede comprobar si un certificado es auténtico. CertiUMET permite:

- Registrar un pedido de certificado y consultar su estado.
- Aprobar o rechazar el pedido y emitir el certificado una sola vez.
- Descargar el certificado en PDF.
- Verificar la autenticidad de un certificado con su código.
- Registrar cada acceso a datos personales en una bitácora.

## Tecnología prevista

Python 3.12 · Django REST Framework · PostgreSQL 16 · Docker Compose · GitHub Actions (hito H4).

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
│   └── matriz-decision.md        Matriz ponderada del estilo
└── 04-registro-ia.md             Registro de uso de IA
```

## Resumen de la arquitectura

- **Estilo:** monolito modular con arquitectura hexagonal ([ADR-003](docs/03-adr/ADR-003-estilo-arquitectonico.md)).
- **Base de datos:** PostgreSQL ([ADR-001](docs/03-adr/ADR-001-base-de-datos-postgresql.md)).
- **Sistema académico:** se consulta solo en lectura, a través de un puerto y un adaptador que se puede cambiar ([ADR-002](docs/03-adr/ADR-002-integracion-sistema-academico.md)).

## Hitos del módulo

| Hito | Contenido | Etiqueta |
|---|---|---|
| H1 | Dossier de arquitectura | `v0.1.0` |
| H2 | Diseño con herramientas CASE | Pendiente |
| H3 | Ramas e implementación de la API | Pendiente |
| H4 | Pipeline de integración y despliegue continuo | Pendiente |
