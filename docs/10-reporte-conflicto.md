# 10 · Reporte del conflicto deliberado

**Fecha:** 29/10/2026 · **Pull requests:** #9 y #10 · **Issues:** #3 y #4 · **Commit de resolución:** `1af9e2a`

## 1. Qué se hizo

Para practicar la resolución de conflictos se crearon dos ramas a la vez desde el mismo commit de `main` (`0e67181`, merge del PR #8), antes de integrar cualquiera:

| Rama | Issue | Pull request | Cambio |
|---|---|---|---|
| `test/3-rechazo-sin-motivo` | #3 | #9 | Criterio nuevo: rechazar un pedido sin motivo responde 422 y el pedido no cambia de estado (commit `ec2f6cc`). |
| `fix/4-error-503-sistema-academico` | #4 | #10 | Respuesta 503 con `Retry-After` cuando el sistema académico no responde al aprobar (commits `37711cc` y `d32cf80`). |

Se integró primero el PR #9 (merge `81adfbb`). Después GitHub mostró en el PR #10 el aviso *"This branch has conflicts that must be resolved"* en tres archivos: `docs/07-historias-y-criterios.md`, `tests/features/hu03.feature` y `tests/test_hu03_resolver_pedido.py`. El archivo `docs/09-revision-de-codigo.md` también cambió en las dos ramas, pero en filas distintas, y Git lo fusionó solo.

## 2. Causa

Las dos ramas agregaron un escenario nuevo al final del bloque de HU-03 y las dos le dieron el mismo identificador, **CA-03.5**. También las dos cambiaron la misma fila de la tabla de trazabilidad de HU-03. Git no puede decidir cuál de las dos versiones es la correcta porque las dos son válidas.

## 3. Marcadores

Al ejecutar `git merge main` en la rama `fix/4` aparecieron estos marcadores en `docs/07-historias-y-criterios.md` (líneas 129 a 143 y 233 a 237):

```text
<<<<<<< HEAD
  @E-06
  Escenario: CA-03.5 Sistema académico sin respuesta al aprobar
    Dado un pedido en estado "VALIDADO"
    Y el sistema académico no responde
    Cuando un funcionario lo aprueba
    Entonces la API responde 503
    Y el pedido sigue en estado "VALIDADO"
    Y no se emite ningún certificado
=======
  Escenario: CA-03.5 Rechazo sin motivo
    Dado un pedido en estado "VALIDADO"
    Cuando un funcionario lo rechaza sin indicar el motivo
    Entonces la API responde 422
    Y el pedido no cambia de estado
>>>>>>> main
```

```text
<<<<<<< HEAD
| HU-03 | E-02, E-04, E-06 | CA-03.1 a CA-03.5 | `PATCH /api/v1/solicitudes/{id}/resolucion` | ADR-001, ADR-003 | |
=======
| HU-03 | E-02, E-04 | CA-03.1 a CA-03.5 | `PATCH /api/v1/solicitudes/{id}/resolucion` | ADR-001, ADR-003 | |
>>>>>>> main
```

- Entre `<<<<<<< HEAD` y `=======` está la versión de la rama actual (`fix/4`).
- Entre `=======` y `>>>>>>> main` está la versión que ya estaba en `main` (PR #9).

## 4. Resolución

Se decidió **mantener los dos criterios**, porque cubren casos distintos:

1. El rechazo sin motivo conserva **CA-03.5**, porque ya estaba integrado en `main`.
2. El escenario del 503 pasa a **CA-03.6** y conserva la etiqueta `@E-06`.
3. La trazabilidad de HU-03 queda: `E-02, E-04, E-06 | CA-03.1 a CA-03.6`, y la fila de medida de E-06 pasa a `CA-01.4 y CA-03.6`.
4. La descripción de la operación en `api/openapi.yaml` se ajustó a "CA-03.1 a CA-03.6".
5. Se regeneraron los archivos `.feature` desde el 07 con `python scripts/extraer_features.py`, se comprobó que no quedaran marcadores (`grep -c "<<<<<<<"` dio 0 en los tres archivos) y se ejecutaron las pruebas: **15 passed**.
6. Commit de merge `1af9e2a` ("Merge main en fix/4: resuelve conflicto CA-03.5 (el 503 pasa a CA-03.6)"), `push` de la rama, CI `pruebas` en verde, autorrevisión con la conversación resuelta y merge del PR #10 (`ed1de18`).

## 5. Prevención

| Regla | Dónde está |
|---|---|
| Reservar el identificador del criterio (CA-0n.m) en el issue antes de crear la rama, para que dos ramas no usen el mismo número. | `CONTRIBUTING.md`, sección 5, y plantilla de historia de usuario |
| Crear la rama desde `main` actualizada y mantenerla corta (horas o pocos días). | `CONTRIBUTING.md`, secciones 1 y 2 |
| Antes de abrir el PR, traer los últimos cambios de `main` (`git merge main`) si otra rama tocó el mismo archivo. | `CONTRIBUTING.md`, sección 5 |
| El CI `pruebas` comprueba que el 07 y los `.feature` coinciden, así que una resolución incompleta no puede entrar a `main`. | `.github/workflows/ci.yml` y regla `proteger-main` |

## 6. Evidencias

Capturas en [`docs/evidencias/semana3/`](evidencias/semana3/README.md):

| Archivo | Muestra |
|---|---|
| `06-pr9-y-pr10-abiertos.png` | Los dos PR abiertos al mismo tiempo |
| `09-pr10-conflicto-github.png` | Aviso de conflicto en el PR #10 con los tres archivos |
| `10-conflicto-merge-local.png` | `git merge main` con `CONFLICT (content)` en tres archivos y fusión automática del 09 |
| `11-conflicto-marcadores.png` | Marcadores `<<<<<<<`, `=======` y `>>>>>>>` en el 07 |
| `12-conflicto-resuelto-pytest.png` | 0 marcadores, CA-03.5 y CA-03.6 en el 07 y 15 pruebas en verde |
| `13-conflicto-status-resuelto.png` | `git status`: *All conflicts fixed but you are still merging* |
| `14-grafo-ramas-merge.png` y `15-grafo-final-main.png` | `git log --graph` con las dos ramas unidas |
