# 08 · Matriz comparativa Git vs SVN

**Proyecto:** CertiUMET API · **Hito:** H3 (`v0.3.0`) · **Decisión relacionada:** [ADR-004](03-adr/ADR-004-control-de-versiones-git.md)

Esta matriz compara Git y Subversion (SVN) con los siete criterios pedidos en la semana 3. Para Git se toma como fuente *Pro Git* (Chacon y Straub, 2014) y para SVN los capítulos 1 y 2 de *Version control with Subversion* (Collins-Sussman et al., 2011). La última columna indica qué significa cada criterio para este proyecto.

## Matriz

| Criterio | Git | SVN | Qué significa para CertiUMET |
|---|---|---|---|
| **Modelo** | Distribuido: cada clon es una copia completa del repositorio con todo su historial. | Centralizado: un solo repositorio en un servidor; cada persona tiene una copia de trabajo (*working copy*) de una versión. | Un desarrollador y el docente como revisor: el modelo distribuido no complica nada y GitHub actúa como copia central. |
| **Historial** | Guarda instantáneas del proyecto; cada commit se identifica con un hash SHA-1 y apunta a su commit padre, lo que forma un grafo. | Cada commit crea un número de revisión global (r1, r2, …) para todo el repositorio. | El grafo de Git deja ver cómo se unieron las ramas del conflicto deliberado (`1af9e2a`, `ed1de18`). |
| **Ramas** | Una rama es un puntero a un commit: crearla y borrarla es inmediato y fusionar es parte del trabajo diario. | Una rama es una copia de una carpeta (`svn copy` a `branches/`); la copia es barata, pero fusionar exige más cuidado. | GitHub Flow usa una rama corta por issue (`chore/1`, `ci/2`, `test/3`, `fix/4`); con SVN ese flujo sería más lento. |
| **Trabajo sin conexión** | Commits, historial, ramas y diferencias funcionan sin red; solo `push` y `pull` la necesitan. | Sin servidor se puede ver el estado y las diferencias de la copia local, pero no se puede hacer commit ni ver el historial. | El estudiante trabaja en WSL y en horarios variables; poder hacer commits sin conexión ayuda mucho. |
| **Permisos** | El acceso es al repositorio completo; la protección se hace en el servidor (por ejemplo, reglas de rama en GitHub). | Permite permisos de lectura y escritura por carpeta en el servidor y bloqueo de archivos (`svn lock`). | Basta con proteger `main` (regla `proteger-main`); no hay carpetas que deban ocultarse a nadie. |
| **Rendimiento** | Casi todas las operaciones son locales y rápidas; el primer clon descarga todo el historial. Los binarios grandes hacen crecer el repositorio. | Cada operación sobre el historial consulta al servidor; es mejor con archivos binarios grandes y repositorios muy grandes, porque solo se descarga lo que se usa. | El repositorio es pequeño y casi todo es texto (código, YAML y Markdown); el rendimiento de Git es suficiente. |
| **Ecosistema** | GitHub, GitLab y Bitbucket; pull requests, GitHub Actions, reglas de rama, Conventional Commits y herramientas de versión semántica. | Herramientas como TortoiseSVN y servidores Apache con `mod_dav_svn`; menos integración con servicios actuales de CI y revisión. | La restricción R7 pide versionar en GitHub con integración continua: solo Git la cumple. |

## Resultado

Para CertiUMET, Git es mejor en cinco de los siete criterios (modelo, historial, ramas, trabajo sin conexión y ecosistema). SVN es mejor en permisos por carpeta y en el manejo de archivos binarios grandes, pero el proyecto no necesita ninguna de las dos cosas. Por eso se mantiene Git con GitHub Flow, decisión registrada en el ADR-004, que también describe en qué caso convendría SVN.

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion* (para Subversion 1.7). https://svnbook.red-bean.com
