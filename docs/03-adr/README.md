# 03 · Registro de decisiones de arquitectura (ADR)

Las decisiones se registran con el formato propuesto por Nygard (2011): título, estado, contexto, decisión y consecuencias. A ese formato se agregan las alternativas consideradas y una sección de **vínculos** con los drivers, escenarios, restricciones y la relación de la vista C4 donde se ve la decisión, para que cada decisión se pueda revisar frente a lo definido en `01-contexto-y-drivers.md`.

| ADR | Decisión | Estado | Escenarios |
|---|---|---|---|
| [ADR-001](ADR-001-base-de-datos-postgresql.md) | Base de datos propia en PostgreSQL | Aceptada | EC-02, EC-04, EC-08 |
| [ADR-002](ADR-002-integracion-sistema-academico.md) | Conexión con el sistema académico mediante puerto y adaptador | Aceptada | EC-05, EC-06, EC-01 |
| [ADR-003](ADR-003-estilo-arquitectonico.md) | Estilo arquitectónico: monolito modular con arquitectura hexagonal (decisión final) | Aceptada | EC-01 a EC-08 |

**Matriz ponderada de la decisión de estilo:** [`matriz-decision.md`](matriz-decision.md)

## Referencias

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
