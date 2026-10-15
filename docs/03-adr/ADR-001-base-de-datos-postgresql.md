# ADR-001 · Base de datos propia en PostgreSQL

**Estado:** Aceptada
**Fecha:** 14/10/2026
**Escenarios relacionados:** EC-02, EC-04, EC-08
**Drivers relacionados:** D2, D1, D5
**Restricciones relacionadas:** R2, R4, R7

## Contexto

La API necesita guardar los pedidos, sus estados, los certificados emitidos y la bitácora de auditoría. Esta información es propia de la API y no debe mezclarse con el sistema académico, porque la Dirección de TI no permite que otros sistemas escriban en él (R2).

Hay dos exigencias que pesan más que el resto:

- **EC-02:** cuando dos funcionarios aprueban el mismo pedido al mismo tiempo, solo debe salir un certificado. La base de datos tiene que manejar operaciones simultáneas sin dejar pasar duplicados.
- **EC-04:** cada operación sobre datos personales debe quedar registrada. Si la operación se guarda pero el registro de bitácora no, se pierde la trazabilidad.

Además, la base de datos debe ser gratuita (R4) y levantarse sin problema en un contenedor dentro de GitHub Actions para el pipeline del hito H4 (R7, EC-08).

## Alternativas consideradas

| Alternativa | A favor | En contra |
|---|---|---|
| **SQLite** | Viene con Python; no necesita servidor | Bloquea toda la base al escribir; con muchas aprobaciones al mismo tiempo no es confiable para EC-02 ni para EC-07 |
| **Oracle Database Free** | Es la misma tecnología del sistema académico y el desarrollador ya la conoce | Imagen de contenedor más pesada y de arranque más lento en el pipeline; mezcla la base de la API con la tecnología del sistema que solo se debe leer |
| **PostgreSQL** | Gratuita; transacciones completas; bloqueo por fila; restricciones `UNIQUE`; soporte oficial en Django; imagen ligera para Docker y GitHub Actions | Es un servicio más que se debe levantar y respaldar |

## Decisión

Se usa **PostgreSQL** como base de datos propia de la API. Para cumplir EC-02 y EC-04 se aplican tres reglas:

1. La tabla de certificados tiene una restricción `UNIQUE` sobre el identificador del pedido. Así, aunque dos aprobaciones lleguen juntas, la base rechaza el segundo certificado.
2. La aprobación lee el pedido con bloqueo de fila (`SELECT ... FOR UPDATE`) dentro de una transacción. La segunda aprobación espera, encuentra el pedido ya aprobado y la API responde `409 Conflict`.
3. El registro en la bitácora se guarda **en la misma transacción** que la operación. Si uno de los dos falla, no se guarda ninguno.

## Consecuencias

**Positivas**

- La regla "un pedido, un solo certificado" queda protegida por la propia base de datos y no solo por el código (EC-02).
- La bitácora no puede quedar incompleta, porque se guarda junto con la operación (EC-04).
- No hay costo de licencias (R4) y el entorno se levanta con un contenedor oficial (EC-08).

**Negativas y riesgos**

- Se agrega un servicio que hay que levantar, respaldar y actualizar.
- El bloqueo de fila hace que la segunda aprobación espere unos milisegundos; con el volumen previsto (A3) este tiempo no es relevante, pero si la demanda creciera mucho debería medirse.
- Las pruebas automáticas deben usar PostgreSQL y no SQLite, porque el comportamiento de los bloqueos es distinto; por ejemplo, una prueba de EC-02 que pasa en SQLite podría no reflejar lo que pasa en producción.

## Referencias

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
