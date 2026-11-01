# Evidencias de la semana 3 · Repositorio gobernado (29/10/2026)

| Archivo | Qué muestra |
|---|---|
| `01-pr7-estructura-abierto.png` | PR #7 `chore: estructura del repositorio gobernado` con `Closes #1` y 4 commits |
| `02-pr8-ci-pruebas-verde.png` | PR #8: job `CI / pruebas` en verde en 1 minuto (`Closes #2`) |
| `03-ruleset-proteger-main-activo.png` | Regla `proteger-main` activa sobre `main`, sin excepciones |
| `04-ruleset-pr-y-conversaciones.png` | PR obligatorio (0 aprobaciones, proyecto individual), conversaciones resueltas y sin borrado de la rama |
| `05-ruleset-check-pruebas-y-force-push.png` | Check `pruebas` obligatorio y bloqueo de `force push` |
| `06-pr9-y-pr10-abiertos.png` | PR #9 y PR #10 abiertos a la vez, creados desde el mismo commit de `main` |
| `07-pr9-merge-bloqueado-conversacion.png` | PR #9 bloqueado hasta resolver la conversación de revisión |
| `08-pr9-check-required-bloqueo.png` | Check `pruebas` marcado como *Required* y merge bloqueado |
| `09-pr10-conflicto-github.png` | PR #10 con conflicto en 3 archivos después de integrar el PR #9 |
| `10-conflicto-merge-local.png` | `git merge main` en la rama `fix/4`: `CONFLICT (content)` en 3 archivos |
| `11-conflicto-marcadores.png` | Marcadores `<<<<<<<`, `=======` y `>>>>>>>` en `docs/07` |
| `12-conflicto-resuelto-pytest.png` | 0 marcadores, CA-03.5 y CA-03.6 en el 07 y 15 pruebas en verde |
| `13-conflicto-status-resuelto.png` | `git status`: *All conflicts fixed but you are still merging* |
| `14-grafo-ramas-merge.png` | `git log --graph` con el commit de resolución `1af9e2a` |
| `15-grafo-final-main.png` | `git log --graph` final de `main` con el merge del PR #10 (`ed1de18`) |
| `16-pr12-dependencias-merged.png` | PR #12 `chore(deps)` integrado, con `Closes #11` (DRF, pytest y pytest-bdd actualizados) |

El rechazo del `push` directo a `main` (error `GH013`) está copiado como texto en `docs/11-revision-seguridad.md`, sección 2.
