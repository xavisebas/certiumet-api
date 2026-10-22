# 02 · Vistas de arquitectura (modelo C4)

Las vistas siguen el modelo C4 (Brown, s. f.) y están escritas como código Mermaid, para que se versionen junto con el resto del repositorio y GitHub las dibuje de forma directa. Cada vista está pensada para un grupo de stakeholders distinto, como recomienda ISO/IEC/IEEE 42010 (ISO/IEC/IEEE, 2022).

| Vista | Archivo | Para quién | Nivel de detalle |
|---|---|---|---|
| Nivel 1 · Contexto | [`nivel-1-contexto.md`](nivel-1-contexto.md) | Secretaría, jefatura, delegado de protección de datos | El sistema como una caja, sin tecnologías |
| Nivel 2 · Contenedores | [`nivel-2-contenedores.md`](nivel-2-contenedores.md) | Desarrollador, Dirección de TI, evaluador técnico | Contenedores con su tecnología y protocolos |

## Reglas que cumplen los diagramas

- Los mismos nombres en los dos niveles y en los documentos `01` y `03` (por ejemplo, "API REST CertiUMET", "Sistema académico", "Correo institucional").
- Todas las flechas tienen una etiqueta que dice qué hace la relación; en el nivel 2 se agrega el protocolo entre corchetes.
- Ninguna caja queda suelta: cada elemento tiene al menos una relación.
- No se mezclan niveles: el nivel 1 no nombra tecnologías y el nivel 2 no muestra módulos internos como cajas.
- Las vistas reflejan la decisión final de estilo (ADR-003): un solo sistema con una API y una base de datos.
- El código Mermaid se probó antes de subirlo, para comprobar que se dibuja sin errores ni líneas cruzadas.

## Revisión cruzada

La instrucción 3 de la actividad pide revisar la consistencia de las vistas con otro equipo. Como el proyecto es individual, la revisión la hace un compañero del módulo con la siguiente lista:

| Pregunta de revisión | Sí / No | Observación |
|---|---|---|
| ¿Los nombres de los elementos son iguales en el nivel 1, el nivel 2, el `01` y los ADR? | | |
| ¿Todas las flechas tienen etiqueta y se entiende qué hacen? | | |
| ¿El nivel 1 evita nombrar tecnologías? | | |
| ¿Cada escenario de calidad (E-01 a E-08) se puede ubicar en algún elemento de las vistas? | | |
| ¿Las vistas muestran el estilo elegido en el ADR-003? | | |
| ¿Los diagramas se ven bien en GitHub (sin errores ni textos encimados)? | | |

**Revisado por:** _(nombre del compañero)_
**Fecha de revisión:** _(fecha)_
**Cambios hechos después de la revisión:** _(describir, o "ninguno")_

## Referencias

Brown, S. (s. f.). *The C4 model for visualising software architecture*. https://c4model.com

ISO/IEC/IEEE. (2022). *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*. International Organization for Standardization.
