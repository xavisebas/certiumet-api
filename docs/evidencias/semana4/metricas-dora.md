# Métricas aproximadas tipo DORA · CertiUMET API

Generado el 09/11/2026 08:36 con `python scripts/metricas_dora.py` sobre la rama main.

## Pull requests integrados en main

| PR | Merge | Fecha del merge | Commits | Tiempo de entrega (h) | Falla en el pipeline |
|---|---|---|---|---|---|
| #7 | 60813ed | 29/10/2026 15:54 | 4 | 0.5 | no |
| #8 | 0e67181 | 29/10/2026 16:27 | 1 | 0.5 | no |
| #9 | 81adfbb | 29/10/2026 17:13 | 1 | 0.5 | no |
| #10 | ed1de18 | 29/10/2026 17:29 | 3 | 0.7 | no |
| #12 | f2c73c8 | 01/11/2026 17:06 | 1 | 0.4 | no |
| #13 | 397c417 | 01/11/2026 17:46 | 5 | 0.4 | no |
| #14 | 7e3f138 | 01/11/2026 17:59 | 1 | 0.1 | no |
| #15 | b1a8b46 | 09/11/2026 08:29 | 5 | 0.5 | sí |

## Entregas (etiquetas SemVer)

| Etiqueta | Fecha |
|---|---|
| `v0.1.0` | 18/10/2026 21:51 |
| `v0.2.0` | 25/10/2026 18:31 |
| `v0.3.0` | 01/11/2026 17:59 |

## Resumen

| Métrica | Valor | Cómo se calculó |
|---|---|---|
| Frecuencia de integración | 5.2 PR por semana (8 PR en 1.5 semanas) | Merges de PR en main desde el primer PR |
| Frecuencia de entrega | 0.9 versiones por semana (3 en 3.5 semanas) | Etiquetas vX.Y.Z desde el primer commit |
| Tiempo de entrega de cambios | mediana 0.5 h (mín. 0.1 h, máx. 0.7 h) | Primer commit de la rama → merge en main |
| Tasa de fallos de cambios | 12 % (1 de 8 PR) | PR con una falla del pipeline corregida antes del merge |
| Tiempo de recuperación | 13 min | Commit que rompió el pipeline → commit que lo corrigió |
| Tasa de retrabajo | 25 % (2 de 8 PR) | PR con commits de tipo fix |
