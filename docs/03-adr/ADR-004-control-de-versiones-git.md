# ADR-004 · Control de versiones con Git y flujo GitHub Flow

**Estado:** Aceptada
**Fecha:** 29/10/2026
**Escenarios relacionados:** E-08
**Drivers relacionados:** D5
**Restricciones relacionadas:** R5, R7

> **Nota de numeración:** la rúbrica de la semana 3 pide registrar esta decisión como ADR-004. El ADR de idioma, que tenía ese número desde la `v0.2.0`, pasa a ser el [ADR-006](ADR-006-idioma-de-los-artefactos.md) sin cambios en su contenido. La etiqueta `v0.2.0` conserva la numeración anterior.

## Contexto

Desde la semana 1 el proyecto se guarda en un repositorio Git en GitHub (restricción R7), pero no había una regla escrita sobre cómo entran los cambios a la rama principal. En las semanas 1 y 2 los commits se hicieron directamente en `main`. En la sesión 8 (semana 3) se pidió decidir y justificar el sistema de control de versiones, el flujo de ramas y las reglas de gobierno del repositorio, comparando Git con Subversion (SVN).

El proyecto lo desarrolla una sola persona (R5) que sigue las clases en diferido, el docente revisa el repositorio como colaborador y el CI de GitHub Actions debe correr en cada cambio. Es importante que cada cambio se pueda seguir desde el issue hasta el commit, y que cada hito quede marcado como línea base (IEEE, 2012).

## Alternativas consideradas

| Alternativa | A favor | En contra |
|---|---|---|
| **SVN** (repositorio central) | Permisos por carpeta; bloqueo de archivos que no se pueden fusionar; números de revisión simples (Collins-Sussman et al., 2011) | Sin servidor no hay historial ni commits; las ramas son copias de carpetas y fusionarlas es más trabajoso; GitHub y GitHub Actions no lo usan, lo que rompe R7 |
| **Git con GitFlow** | Ramas `develop`, `release` y `hotfix` para mantener varias versiones a la vez | Ramas de larga duración que aumentan los conflictos; el proyecto publica una sola versión por hito |
| **Git con trunk-based development** | Integración varias veces al día; mejor relación con las métricas DORA (Forsgren et al., 2018) | Sin pull request no queda la revisión escrita ni la traza issue → PR → commit que pide el módulo |
| **Git con GitHub Flow** | Una sola rama estable (`main`) y ramas cortas por issue; revisión y CI en cada pull request; hotfix simple desde `main` | Depende de que el CI y la protección de `main` estén bien configurados |

La comparación completa entre Git y SVN está en [`08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md).

## Decisión

Se usa **Git en GitHub con el flujo GitHub Flow**, con estas reglas (detalladas en `CONTRIBUTING.md`):

- Todo cambio nace en un issue, se trabaja en una rama corta `<tipo>/<n>-<descripcion>` creada desde `main` actualizada y entra por pull request con `Closes #n`.
- Mensajes de commit con Conventional Commits 1.0.0 y versiones con SemVer 2.0.0: una etiqueta anotada por hito (`v0.1.0`, `v0.2.0`, `v0.3.0`).
- `main` protegida con la regla `proteger-main`: pull request obligatorio, check `pruebas` del CI obligatorio, conversaciones resueltas antes del merge, sin `force push` y sin borrado de la rama.
- Integración con *merge commit*, para conservar los commits atómicos de cada rama.
- Proyecto individual: la regla exige 0 aprobaciones, porque GitHub no permite aprobar un pull request propio; la revisión cruzada se reemplaza por una autorrevisión escrita en cada PR.

## Consecuencias

**Positivas**

- Cada cambio desde la sesión 8 se puede seguir de issue a PR y a commit (PR #7 a #10 y #12).
- La protección se comprobó: un `push` directo a `main` fue rechazado con el error `GH013` y el PR #9 no se pudo integrar hasta resolver la conversación de revisión.
- El conflicto deliberado entre los PR #9 y #10 se detectó en el pull request y se resolvió en local sin afectar `main` (ver `10-reporte-conflicto.md`).
- Todo el historial está en la computadora del desarrollador, por lo que se puede trabajar sin conexión.

**Negativas y riesgos**

- Sin un segundo integrante no hay revisión cruzada real; si el equipo crece, se activa "1 aprobación obligatoria" en la misma regla.
- Git no tiene permisos de lectura por carpeta: quien puede leer el repositorio lo ve completo.
- Los archivos binarios grandes (por ejemplo, PDF de certificados de prueba) no deben versionarse; si llegan a ser necesarios, se evalúa Git LFS.

## Cuándo convendría SVN

SVN sería la mejor opción en un proyecto con muchos archivos binarios que no se pueden fusionar (planos, diseños o recursos de videojuegos), donde es necesario bloquear el archivo mientras una persona lo edita, o en una organización que necesita dar permisos de lectura distintos por carpeta dentro del mismo repositorio y que ya trabaja con un servidor central (Collins-Sussman et al., 2011). Ninguno de esos casos aplica a CertiUMET.

## Vínculos

| Tipo | Elemento |
|---|---|
| Drivers | D5 (despliegue sencillo, repetible y de bajo costo) |
| Escenarios | E-08 (instalación del entorno desde cero en la integración continua) |
| Restricciones | R5 (una sola persona), R7 (versionar en GitHub, listo para integración continua) |
| Artefactos | `CONTRIBUTING.md`, `.github/`, `08-matriz-git-vs-svn.md`, `10-reporte-conflicto.md`, `11-revision-seguridad.md` |

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion* (para Subversion 1.7). https://svnbook.red-bean.com

Conventional Commits. (s. f.). *Conventional Commits 1.0.0*. https://www.conventionalcommits.org/es/v1.0.0/

Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The science of lean software and DevOps*. IT Revolution Press.

IEEE. (2012). *IEEE standard for configuration management in systems and software engineering* (IEEE Std 828-2012). IEEE.

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

Preston-Werner, T. (s. f.). *Versionado semántico 2.0.0*. https://semver.org/lang/es/
