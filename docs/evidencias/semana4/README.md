# Evidencias de la semana 4 · Pipeline con quality gates (09/11/2026)

| Archivo | Qué muestra |
|---|---|
| `01-pr15-abierto.png` | PR #15 `ci: pipeline con seis quality gates` con la tabla de las seis puertas |
| `02-pr15-falla-puerta-calidad.png` | Primera ejecución: la puerta `calidad` falla (ruff E501 en `scripts/metricas_dora.py`) y `pruebas` no se ejecuta porque depende de ella |
| `03-ruleset-seis-checks.png` | Regla `proteger-main` con los seis checks obligatorios |
| `04-pr15-autorrevision-workflow.png` | Autorrevisión del workflow con la lista de verificación (permisos, versiones, secretos, `timeout`, `needs`) |
| `05-pr15-seis-checks-verdes-merged.png` | Después del commit `7168a82` (`fix(ci)`), los seis checks en verde y el PR integrado |
| `metricas-dora.md` | Salida de `python scripts/metricas_dora.py` sobre `main` (commit `b1a8b46`) |

Salida local del error, antes de la corrección:

```text
E501 Line too long (127 > 120)
  --> scripts/metricas_dora.py:77:121
Found 1 error.
```
