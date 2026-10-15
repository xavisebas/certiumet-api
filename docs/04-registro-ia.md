# 04 · Registro de uso de inteligencia artificial

**Herramienta:** Claude (Anthropic), modelo Claude Opus 5.5, versión web, octubre de 2026
**Responsable de la revisión:** Xavier Guaygua
**Regla aplicada:** no se ingresaron datos personales reales, credenciales ni información interna de la universidad. Todos los datos del caso (cifras de estudiantes, pedidos y personas) son supuestos o ficticios (supuesto A4).

La IA se usó como apoyo para redactar, ordenar y revisar. Las decisiones del caso (tema, base de datos, alcance y trabajo individual) las tomó el estudiante, y cada salida se contrastó con la transcripción de las clases, la rúbrica y la bibliografía del módulo antes de aceptarla.

## Registro

| N.º | Fecha | Actividad | Prompt resumido | Salida de la IA | Verificación | Resultado |
|---|---|---|---|---|---|---|
| 1 | 14/10/2026 | Elección del caso | Proponer temas para una API pequeña (unos 4 endpoints) que sirva para las cuatro semanas del módulo | Tres opciones: turnos (TurnoFácil), certificados académicos de la Secretaría y pedidos de un taller de confección | Se comparó con lo pedido en la clase del 12/10 (API pequeña, caso libre). Se descartó TurnoFácil por ser casi igual al ejemplo del docente | **Aceptado** el tema de certificados; **rechazadas** las otras dos opciones |
| 2 | 14/10/2026 | Base de datos | Preguntar qué base de datos usar, dado que la Secretaría trabaja con Oracle | Recomendación de PostgreSQL y simular el sistema académico | Se revisó la transcripción: el docente no fijó una base de datos y pidió bajo costo, software libre y despliegue sencillo | **Aceptado**; se registró como ADR-001 |
| 3 | 14/10/2026 | `01-contexto-y-drivers.md` | Redactar stakeholders, restricciones, drivers y 5 o más escenarios de seis partes según la rúbrica | Primera versión con 7 stakeholders, 7 restricciones, 6 drivers y 8 escenarios | Se revisó cada escenario contra la rúbrica ("un solo atributo por escenario"). En EC-02, EC-03, EC-04 y EC-08 había medidas de tiempo o costo que pertenecían a otro atributo | **Modificado**: se quitaron esas medidas mezcladas |
| 4 | 14/10/2026 | Referencias | Comprobar los datos de las referencias de la bibliografía del módulo | Datos de Nygard (2011), ISO/IEC 25010:2023 y la Ley Orgánica de Protección de Datos Personales | Se comprobaron en fuentes web: título completo de ISO/IEC 25010:2023 y sus características; fecha y enlace del artículo de Nygard; Registro Oficial Suplemento 459 de la ley | **Aceptado** después de verificar |
| 5 | 14/10/2026 | Redacción | Reescribir el 01 con palabras sencillas y en forma impersonal | Versión con lenguaje más común ("el 95 % de las respuestas en menos de 2 segundos" en lugar de "p95") | Se revisó que no quedaran frases en primera persona ni términos rebuscados | **Modificado**: se ajustaron frases a la forma de escribir del estudiante |
| 6 | 14/10/2026 | ADR-001, ADR-002 y ADR-003 | Redactar los ADR con contexto, alternativas, decisión y consecuencias, unidos a los escenarios | Tres ADR en formato Nygard con alternativas y consecuencias positivas y negativas | Se comparó con el mínimo pedido en la clase del 14/10 (código, título, estado, contexto, decisión, alternativas, consecuencias y respaldo) | **Aceptado** |
| 7 | 14/10/2026 | Matriz ponderada | Comparar tres estilos frente a los escenarios con pesos | Matriz con pesos por prioridad y calificaciones de 1 a 5 justificadas | Los puntajes se recalcularon con un script (A 4,50; C 3,65; B 3,42) y se hizo una prueba de sensibilidad duplicando los pesos de EC-06 y EC-07 | **Aceptado**; se agregó la prueba de sensibilidad |
| 8 | 15/10/2026 | Vistas C4 | Generar el código Mermaid del nivel 1 y nivel 2 a partir del contexto y los ADR | Dos diagramas en Mermaid | Se dibujaron con Mermaid antes de subirlos. En el nivel 2 aparecían líneas y etiquetas cruzadas, algo que el docente pidió evitar | **Modificado**: la tarea programada pasó a ejecutarse dentro del contenedor de la API, se acortaron etiquetas y se reordenaron elementos. Se actualizaron el 01, el ADR-003 y la matriz para que digan lo mismo |
| 9 | 15/10/2026 | Consistencia | Revisar que los nombres y cantidades coincidan en todos los documentos | Lista de diferencias (número de contenedores en EC-08, ADR-003 y matriz) | Se buscaron las menciones en todos los archivos | **Modificado**: se unificaron los textos |

## Lo que no se aceptó de la IA

- Ningún dato numérico del caso se tomó como real: las cifras del supuesto A3 son estimaciones y quedan marcadas como supuestos.
- La revisión cruzada de las vistas (instrucción 3) no la hizo la IA; la debe hacer un compañero del módulo (ver `02-vistas-c4/README.md`).
- Las opciones de tema y de base de datos que no se ajustaban al caso se rechazaron (filas 1 y 2).
