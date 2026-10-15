# ADR-003 · Estilo arquitectónico: monolito modular con arquitectura hexagonal

**Estado:** Aceptada (decisión final de estilo)
**Fecha:** 14/10/2026
**Escenarios relacionados:** EC-01 a EC-08
**Drivers relacionados:** D1, D2, D3, D4, D5
**Decisiones previas que lo apoyan:** ADR-001, ADR-002
**Evidencia:** [`matriz-decision.md`](matriz-decision.md)

## Contexto

Con los drivers ya priorizados (`01-contexto-y-drivers.md`), falta elegir el estilo general de la API. Esta es la decisión más difícil de cambiar después: si se elige mal, hay que reorganizar todo el código y el despliegue (Bass et al., 2021).

Los dos drivers de mayor prioridad son D1 (proteger calificaciones y registrar accesos) y D2 (un solo certificado por pedido y verificable). Los dos necesitan que la operación y su registro se guarden juntos y sin duplicados. Por otro lado, D3 pide que la conexión con el sistema académico se pueda cambiar sin afectar al resto. Todo esto debe hacerlo un equipo de una sola persona en cuatro semanas (R5), con software libre (R4) y con un despliegue sencillo (D5).

## Alternativas consideradas

Se compararon tres alternativas con una matriz ponderada frente a los escenarios EC-01 a EC-08 ([`matriz-decision.md`](matriz-decision.md)):

| Alternativa | Puntaje (sobre 5) |
|---|---|
| A · Monolito modular con arquitectura hexagonal | **4,50** |
| C · Monolito en capas tradicional | 3,65 |
| B · Microservicios | 3,42 |

## Decisión

Se adopta un **monolito modular con arquitectura hexagonal** (puertos y adaptadores):

- **Un solo despliegue:** un proyecto Django REST Framework en un contenedor, con una base PostgreSQL (ADR-001).
- **Módulos con límites claros**, cada uno como una aplicación de Django: `solicitudes`, `emision` (incluye la verificación), `auditoria`, `integracion_academica` y `notificaciones`. Un módulo no accede a las tablas de otro, solo a sus servicios.
- **Hexagonal por dentro:** la lógica de negocio (dominio y casos de uso) no depende de Django ni de la base de datos. Se comunica con el exterior por puertos, por ejemplo `ProveedorDatosAcademicos` (ADR-002), `RepositorioSolicitudes` y `ServicioNotificaciones`.
- **Seguridad en un solo punto:** el control de acceso por dueño del pedido y el registro en la bitácora se hacen en la capa de casos de uso, para que ninguna operación se los salte (EC-01, EC-04).
- **Verificación de certificados:** cada certificado lleva un código firmado con HMAC-SHA256 usando una clave que solo conoce el servidor. Así, un código alterado se detecta sin consultar datos personales (EC-03).

## Consecuencias

**Positivas**

- EC-02 y EC-04 se resuelven con una transacción local, que es la forma más simple y segura para un equipo pequeño.
- Cambiar el servicio académico simulado por el real afecta a un solo adaptador (EC-05).
- El despliegue es un solo `docker-compose.yml` (API con su tarea programada, PostgreSQL, servicio académico simulado y SMTP de pruebas), fácil de repetir en el pipeline de integración continua (EC-08).
- Los módulos con límites claros dejan abierta la puerta para separar uno en servicio aparte en el futuro, si la demanda creciera; por ejemplo, el módulo de verificación, que es público.

**Negativas y riesgos (trade-off)**

- Se acepta perder algo de aislamiento ante fallos y de escalado por partes frente a microservicios (EC-06 y EC-07). Si una parte falla gravemente, puede afectar al proceso completo. Se considera aceptable por el volumen bajo (A3).
- Hay más código inicial que en un monolito en capas, por los puertos y adaptadores.
- Los límites entre módulos dependen de la disciplina del desarrollador, porque Django no impide que un módulo importe a otro. Para controlarlo se revisarán las dependencias en las revisiones de código (pull requests) del hito H3.

## Referencias

Bass, L., Clements, P., & Kazman, R. (2021). *Software architecture in practice* (4.ª ed.). Addison-Wesley.

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

Richards, M., & Ford, N. (2020). *Fundamentals of software architecture: An engineering approach*. O'Reilly Media.
