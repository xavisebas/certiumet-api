# ADR-002 · Conexión con el sistema académico mediante puerto y adaptador

**Estado:** Aceptada
**Fecha:** 14/10/2026
**Escenarios relacionados:** EC-05, EC-06, EC-01
**Drivers relacionados:** D3, D1
**Restricciones relacionadas:** R1, R2
**Supuestos relacionados:** A1

## Contexto

Para revisar un pedido y armar el certificado, la API necesita los datos del estudiante y sus calificaciones. Esos datos están en el sistema académico de la universidad, que es la única fuente oficial (R2). En el proyecto no se puede usar ese sistema real, así que se trabaja con un servicio simulado con datos ficticios (A1). Sin embargo, en un caso real la conexión tendría que cambiarse por la del sistema académico (Oracle).

Esto deja tres necesidades:

- **EC-05:** cambiar el servicio simulado por el real sin rehacer la API.
- **EC-06:** si el sistema académico se cae, la API no debe perder pedidos ni dejar de mostrar su estado.
- **R1 y EC-01:** traer solo los datos necesarios, para no guardar más información personal de la que hace falta.

## Alternativas consideradas

| Alternativa | A favor | En contra |
|---|---|---|
| **Consulta directa desde las vistas de la API** | Es lo más rápido de programar | El código de negocio queda amarrado al sistema académico; cambiar de simulado a Oracle obliga a tocar muchas partes (falla EC-05); si el sistema académico se cae, el pedido falla (falla EC-06) |
| **Copiar la base académica a PostgreSQL cada noche** | La API no depende del sistema académico en línea | Duplica calificaciones de todos los estudiantes, aunque no pidan nada (choca con R1); los datos pueden estar desactualizados hasta el día siguiente |
| **Puerto y adaptador con reintentos** | El negocio solo conoce una interfaz; se cambia el adaptador y nada más; los fallos se manejan en un solo lugar | Más trabajo inicial: se programa una interfaz y al menos dos adaptadores |

## Decisión

Se define un **puerto** (una interfaz), llamado `ProveedorDatosAcademicos`, con solo dos operaciones: obtener los datos básicos del estudiante y obtener las calificaciones para un tipo de certificado. La lógica de negocio solo conoce este puerto.

Se programan dos **adaptadores**:

1. `AdaptadorAcademicoSimulado`: llama por HTTP al servicio simulado con datos ficticios. Es el que se usa en el proyecto y en el pipeline.
2. `AdaptadorAcademicoOracle`: queda definido como el reemplazo para un caso real, con acceso de solo lectura a una vista del sistema académico.

El adaptador que se usa se elige con una variable de entorno, sin cambiar código.

Para EC-06, cada llamada tiene un tiempo máximo de espera de 3 segundos. Si el sistema académico no responde, el pedido queda en `EN_VALIDACION` y una tarea programada lo vuelve a intentar cada 5 minutos, hasta 6 veces. Si después de eso sigue sin respuesta, el pedido pasa a revisión manual del funcionario.

Para R1, las calificaciones **no se guardan** en PostgreSQL. Se piden en el momento de emitir el certificado y solo quedan dentro del PDF. En la base se guarda el código de verificación y un resumen criptográfico (hash) del documento.

## Consecuencias

**Positivas**

- Cambiar de servicio simulado a Oracle afecta solo a un adaptador (EC-05).
- Una caída del sistema académico no hace perder pedidos; solo retrasa su validación (EC-06).
- La API guarda menos datos personales, lo que reduce el daño si algún día hubiera una filtración (R1, EC-01).
- En las pruebas es sencillo reemplazar el adaptador por uno falso para simular fallos.

**Negativas y riesgos**

- Hay más archivos y más código al inicio que con una consulta directa.
- Si las calificaciones cambian entre la aprobación y la descarga, el PDF muestra las del momento de la emisión. Es el comportamiento esperado de un certificado, pero debe quedar claro para la Secretaría.
- El adaptador de Oracle no se puede probar contra el sistema real dentro del proyecto; solo se prueba que cumple el puerto.

## Referencias

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

Richards, M., & Ford, N. (2020). *Fundamentals of software architecture: An engineering approach*. O'Reilly Media.
