# 03 · Registro de decisiones de arquitectura (ADR)

Las decisiones se registran con el formato propuesto por Nygard (2011): título, estado, contexto, decisión y consecuencias. A ese formato se agregan las alternativas consideradas y una sección de **vínculos** con los drivers, escenarios, restricciones y la relación de la vista C4 donde se ve la decisión, para que cada decisión se pueda revisar frente a lo definido en `01-contexto-y-drivers.md`.

| ADR | Decisión | Estado | Escenarios |
|---|---|---|---|
| [ADR-001](ADR-001-base-de-datos-postgresql.md) | Base de datos propia en PostgreSQL | Aceptada | E-02, E-04, E-08 |
| [ADR-002](ADR-002-integracion-sistema-academico.md) | Conexión con el sistema académico mediante puerto y adaptador | Aceptada | E-05, E-06, E-01 |
| [ADR-003](ADR-003-estilo-arquitectonico.md) | Estilo arquitectónico: monolito modular con arquitectura hexagonal (decisión final) | Aceptada | E-01 a E-08 |
| [ADR-004](ADR-004-idioma-de-los-artefactos.md) | Idioma de los artefactos: lenguaje del negocio en español y términos técnicos del framework en inglés | Aceptada | E-05 |

**Matriz ponderada de la decisión de estilo:** [`matriz-decision.md`](matriz-decision.md)

## Referencias

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
