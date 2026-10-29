# Cómo contribuir a CertiUMET API

Este documento explica cómo se manejan las ramas, los commits y los pull requests (PR) del repositorio. Las reglas siguen el flujo **GitHub Flow** decidido en el ADR-004 y se aplican desde la sesión 8 (semana 3).

## 1. Flujo de trabajo

```
issue (#n)  →  rama corta desde main  →  commits convencionales  →  PR con "Closes #n"
            →  CI en verde + revisión  →  merge a main  →  se borra la rama
```

1. **Todo cambio empieza en un issue.** Las historias de usuario usan la plantilla *Historia de usuario* (HU-0n) y el resto de cambios la plantilla *Tarea técnica*.
2. **Una rama por issue**, creada desde `main` actualizada:
   ```bash
   git switch main && git pull
   git switch -c <tipo>/<n>-<descripcion-corta>
   ```
3. **Commits pequeños y frecuentes** con Conventional Commits (sección 3).
4. **Se abre un PR hacia `main`** con la plantilla del repositorio y la línea `Closes #n` para cerrar el issue al integrar.
5. **El PR solo se integra si** el CI (`pruebas`) está en verde y la revisión no tiene comentarios sin resolver.
6. **Después del merge** la rama se borra (GitHub la elimina automáticamente).

`main` está protegida: no acepta commits directos ni `force push`; los cambios entran solo por PR.

## 2. Nombres de ramas

| Tipo de rama | Uso | Ejemplo |
|---|---|---|
| `feat/` | Nueva funcionalidad o historia de usuario | `feat/7-descarga-certificado` |
| `fix/` | Corrección de un error | `fix/4-error-503-sistema-academico` |
| `test/` | Solo pruebas o criterios | `test/3-rechazo-sin-motivo` |
| `docs/` | Documentación, ADR, historias | `docs/5-matriz-git-svn` |
| `ci/` | Integración continua | `ci/2-integracion-continua` |
| `chore/` | Mantenimiento (estructura, dependencias) | `chore/1-repositorio-gobernado` |

Las ramas viven horas o pocos días, no semanas.

## 3. Mensajes de commit (Conventional Commits 1.0.0)

```
<tipo>(<ámbito opcional>): <descripción en español, en minúsculas y sin punto final>
```

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Funcionalidad nueva (sube la versión MENOR) |
| `fix` | Corrección de un error (sube la versión de PARCHE) |
| `docs` | Documentación, ADR, historias y criterios |
| `test` | Pruebas nuevas o corregidas |
| `refactor` | Cambio de código que no cambia el comportamiento |
| `ci` | Archivos de GitHub Actions |
| `chore` | Mantenimiento: estructura, `.gitignore`, dependencias |

Ejemplos: `feat(emision): responde 503 cuando el sistema académico no responde`, `test(hu03): agrega CA-03.5 de rechazo sin motivo`, `docs(adr): agrega ADR-004 de control de versiones`.

Un commit = un cambio lógico. Si un trabajo se hace con ayuda de IA, se hace commit antes de cada nueva instrucción para poder ver qué cambió la IA, y se registra en `docs/04-registro-ia.md`.

## 4. Pull requests y revisión

- Título con el mismo formato de Conventional Commits.
- Descripción con la plantilla: qué cambia, issue (`Closes #n`), cómo se probó y lista de verificación.
- **Revisión:** cada PR tiene una revisión escrita en la pestaña *Files changed* de GitHub (*Review changes → Comment*), con comentarios sustantivos sobre las líneas que cambian: criterio de aceptación, contrato, riesgos y pruebas. Los comentarios que piden un cambio se corrigen con un nuevo commit en la misma rama y se marcan como resueltos antes del merge.
- **Proyecto individual (nota para el docente):** el proyecto se desarrolla de forma individual, porque las clases se siguen en diferido por motivos de trabajo y no fue posible coordinar con un compañero del módulo. Por eso la revisión cruzada se reemplaza por una **autorrevisión escrita** del autor en cada PR, con la lista de verificación de la plantilla y comentarios en las líneas revisadas. GitHub no permite aprobar el PR propio, así que la regla de `main` exige PR, CI en verde y conversaciones resueltas, pero no una aprobación de otra persona. Si el equipo crece, se activa "1 aprobación obligatoria" en la misma regla.
- **Integración:** *Create a merge commit*, para que el historial conserve los commits atómicos de la rama.

## 5. Conflictos

Si al integrar aparece un conflicto:

1. Actualizar la rama con `main` (`git switch <rama> && git merge main`).
2. Leer los marcadores `<<<<<<<`, `=======` y `>>>>>>>` y decidir qué queda (un cambio, el otro o una versión que una los dos).
3. Quitar los marcadores, ejecutar `bash scripts/cadena.sh` y hacer el commit de merge.
4. Documentar en `docs/10-reporte-conflicto.md`: causa, marcadores, resolución y cómo prevenirlo.

## 6. Versiones (SemVer 2.0.0)

`MAYOR.MENOR.PARCHE`. Cada hito del módulo tiene su etiqueta anotada sobre el commit de cierre del hito en `main`:

| Hito | Etiqueta |
|---|---|
| H1 · Dossier de arquitectura | `v0.1.0` |
| H2 · Cadena CASE | `v0.2.0` |
| H3 · Repositorio gobernado | `v0.3.0` |

Mientras la versión mayor sea 0, el contrato puede cambiar. Una corrección urgente sobre una versión publicada sale de `main` en una rama `fix/` y sube el PARCHE (por ejemplo, `v0.3.1`).

## 7. Seguridad

- Nunca se versionan claves, contraseñas ni archivos `.env`; los valores reales van en variables de entorno.
- No se suben entornos virtuales, bases locales ni archivos generados (ver `.gitignore`).
- Las dependencias se revisan con `pip-audit` antes de cada versión (`docs/11-revision-seguridad.md`).
- No se ingresan datos personales ni credenciales en herramientas de IA.
