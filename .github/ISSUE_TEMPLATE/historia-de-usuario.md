---
name: Historia de usuario
about: Nueva historia de usuario (HU) con sus criterios de aceptación
title: "HU-0n · <acción del usuario>"
labels: historia-de-usuario
---

## Historia

**Como** <rol>, **quiero** <acción>, **para** <beneficio>.

## Trazabilidad

| Stakeholder | Driver | Escenario de calidad | Endpoint | ADR |
|---|---|---|---|---|
| S? | D? | E-0? | `MÉTODO /api/v1/...` | ADR-00? |

## Criterios de aceptación (Gherkin)

```gherkin
# language: es
@HU-0n
Escenario: CA-0n.m <nombre>
  Dado <condición inicial>
  Cuando <acción>
  Entonces <resultado con su medida>
```

## Definición de terminado

- [ ] Criterios agregados en `docs/07-historias-y-criterios.md` y `.feature` regenerados (`python scripts/extraer_features.py`)
- [ ] Contrato `api/openapi.yaml` actualizado y Spectral sin errores
- [ ] Pruebas de los criterios en `tests/` pasando en PostgreSQL
- [ ] Uso de IA registrado en `docs/04-registro-ia.md` (si aplica)
