# 11 · Revisión de gobierno y seguridad del repositorio

**Fecha:** 29/10/2026 · **Hito:** H3 (`v0.3.0`) · **Rúbrica:** instrucciones 5 y 6 de la actividad autónoma de la semana 3

La revisión sigue tres prácticas del marco SSDF del NIST (Souppaya et al., 2022): proteger el código contra cambios no autorizados (PS.1), reutilizar software de terceros que esté bien mantenido (PW.4) e identificar vulnerabilidades de forma continua (RV.1).

## 1. Todo cambio desde la sesión 8 entró por pull request

Comando usado: `git log --first-parent --oneline main` (muestra solo los commits que llegaron directamente a `main`).

| Commit en `main` | Pull request | Issue | Rama | CI `pruebas` | Revisión |
|---|---|---|---|---|---|
| `60813ed` | #7 | #1 | `chore/1-repositorio-gobernado` | No existía aún (llega en el #8) | Autorrevisión con 2 comentarios |
| `0e67181` | #8 | #2 | `ci/2-integracion-continua` | Verde | Autorrevisión |
| `81adfbb` | #9 | #3 | `test/3-rechazo-sin-motivo` | Verde (obligatorio) | Autorrevisión; conversación resuelta |
| `ed1de18` | #10 | #4 | `fix/4-error-503-sistema-academico` | Verde (obligatorio) | Autorrevisión; conflicto resuelto |
| (merge del #12) | #12 | #11 | `chore/11-actualizar-dependencias` | Verde (obligatorio) | Autorrevisión |

Desde el commit `60813ed` no hay commits directos en `main`: todos son merges de pull requests. Los commits anteriores (`9915ac0` a `bff63d0`, etiquetas `v0.1.0` y `v0.2.0`) son de las semanas 1 y 2, antes de que se definiera el flujo.

## 2. Protección de `main`

Regla `proteger-main` (Settings → Rules → Rulesets), activa sobre la rama por defecto y sin excepciones (*bypass list* vacía):

| Regla | Valor |
|---|---|
| Require a pull request before merging | Sí, 0 aprobaciones (proyecto individual) |
| Require conversation resolution before merging | Sí |
| Require status checks to pass | Sí, check `pruebas` de GitHub Actions |
| Block force pushes | Sí |
| Restrict deletions | Sí |

**Prueba:** un commit vacío enviado directo a `main` fue rechazado:

```text
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - Required status check "pruebas" is expected.
 ! [remote rejected] main -> main (push declined due to repository rule violations)
```

El commit de prueba se borró con `git reset --hard origin/main`. Evidencias: `03` a `05`, `07` y `08` en `docs/evidencias/semana3/`.

## 3. Secretos

| Revisión | Resultado |
|---|---|
| Búsqueda en todo el historial: `git log --all -p \| grep -i -E "password\s*=\|secret_key\s*=\|token\s*="` (sin las variables `POSTGRES_PASSWORD` y las lecturas de `environ`) | Solo aparecen textos de ejemplo (`YOUR_ACCESS_TOKEN`) en los clientes que genera OpenAPI Generator y en la librería `marked.js` de la documentación HTML. No hay claves reales. |
| Archivos generados (`api/stubs/`, `docs/api/`) | Dejaron de versionarse en el PR #7 (`.gitignore`). |
| `.env`, entornos virtuales y bases locales | Excluidos en `.gitignore`. |
| Clave de PostgreSQL en `ci.yml` (`certiumet_ci`) | Solo sirve para la base temporal del job de CI, que se borra al terminar; no es una credencial real. |
| Clave local de PostgreSQL | Se pasa por variable de entorno (`POSTGRES_PASSWORD`); el README usa `<clave local>`. |
| Token de GitHub | No está en el repositorio ni en la URL del remoto; se guarda en el gestor de credenciales de Git del equipo del estudiante. |

## 4. Dependencias

Herramienta: `pip-audit -r requirements-dev.txt`.

**Antes (29/10/2026):** 7 vulnerabilidades conocidas en 2 paquetes.

| Paquete | Versión | Identificadores | Versión que lo corrige |
|---|---|---|---|
| djangorestframework | 3.16.1 | PYSEC-2026-3827, PYSEC-2026-3828 | 3.17.2 |
| djangorestframework | 3.16.1 | CVE-2026-114136, CVE-2026-114137, CVE-2026-114138 | 3.18.2 |
| pytest | 8.4.2 | PYSEC-2026-1845 (aparece dos veces) | 9.0.3 |

**Acción:** issue #11 y PR #12 (`chore(deps)`): `djangorestframework>=3.18.2,<3.19`, `pytest>=9.0.3,<10` y `pytest-bdd>=9.0.1,<10`.

**Problema encontrado al actualizar:** con el rango nuevo se instaló pytest 9.2.0, y las 16 pruebas fallaron con `AttributeError: 'FixtureManager' object has no attribute '_arg2fixturedefs'`, porque pytest-bdd 8.1 usa una parte interna de pytest que cambió. Se actualizó también pytest-bdd a 9.0.1, que es compatible. Este caso muestra por qué una actualización de dependencias debe pasar por las pruebas antes de entrar a `main`.

**Después:** `No known vulnerabilities found`. Con djangorestframework 3.18.3, pytest 9.2.0 y pytest-bdd 9.0.1 pasan las 15 pruebas (Python 3.10 en local y 3.12 en el CI), ruff no reporta errores e import-linter cumple los 3 contratos.

**Regla:** pip-audit se ejecuta antes de cada etiqueta de versión (`CONTRIBUTING.md`, sección 7).

## 5. Pendientes

- Activar Dependabot o agregar `pip-audit` como paso del CI para que la revisión de dependencias no dependa de hacerla a mano (hito H4).
- Si el equipo crece, exigir 1 aprobación en la regla `proteger-main`.

## Referencias

Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1: Recommendations for mitigating the risk of software vulnerabilities* (NIST Special Publication 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
