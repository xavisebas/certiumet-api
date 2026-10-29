# 07 · Historias de usuario y criterios de aceptación

**Proyecto:** CertiUMET API · **Semana:** 2 · **Fecha:** 22/10/2026
**Documentos relacionados:** `01-contexto-y-drivers.md` (S, D, CU-01 a CU-05 y E-01 a E-08), `03-adr/`, `06-mapa-toolchain.md` (T01, T02 y T04), `api/openapi.yaml`

Este documento parte de los escenarios de calidad del dossier y llega a los criterios que después se convierten en pruebas. Los requisitos se revisan con los atributos de un buen requisito de ISO/IEC/IEEE 29148 (ISO/IEC/IEEE, 2018) y los criterios se escriben en Gherkin, el formato Dado / Cuando / Entonces de la práctica BDD (Smart, 2014). Según el ADR-004, los criterios se escriben en español con la cabecera `# language: es`.

**Identificadores nuevos:** HU = historia de usuario (HU-01 a HU-05, una por caso de uso CU-01 a CU-05); CA = criterio de aceptación (CA-0n.m, donde *n* es la historia y *m* el criterio). Cada escenario Gherkin lleva la etiqueta `@HU-0n` y la del escenario de calidad que verifica (por ejemplo, `@E-02`), para unir la prueba con su historia.

## Paso 1 · De los escenarios a las historias

| ID | Historia | Stakeholder | Driver · escenario |
|---|---|---|---|
| HU-01 | Como estudiante, quiero pedir un certificado académico en línea, para no tener que ir a la ventanilla de la Secretaría. | S1 | D6, D4 · E-07 (E-06 como extensión) |
| HU-02 | Como estudiante, quiero consultar el estado de mi pedido, para saber cuándo estará listo mi certificado. | S1, S4 | D1 · E-01, E-04 |
| HU-03 | Como funcionario de Secretaría, quiero aprobar o rechazar un pedido, para que el certificado se emita una sola vez y solo cuando corresponde. | S2 | D2, D1 · E-02, E-04 |
| HU-04 | Como estudiante, quiero descargar mi certificado en PDF, para presentarlo donde lo necesite. | S1, S4 | D1 · E-01, E-04 |
| HU-05 | Como entidad externa, quiero comprobar un certificado con su código, para saber si es auténtico sin llamar a la universidad. | S5 | D2 · E-03 |

**Estados del pedido** (se usan en los criterios y en el contrato): `EN_VALIDACION` → `VALIDADO` → `APROBADO` o `RECHAZADO`. Un pedido pasa a `VALIDADO` cuando el sistema académico confirma que el estudiante cumple los requisitos.

## Paso 2 · Criterios de aceptación en Gherkin

### HU-01 · Pedir un certificado

```gherkin
# language: es
@HU-01
Característica: Pedir un certificado académico
  Como estudiante
  Quiero pedir un certificado académico en línea
  Para no tener que ir a la ventanilla de la Secretaría

  Escenario: CA-01.1 Pedido válido
    Dado un estudiante con sesión iniciada
    Cuando pide un "certificado de matrícula"
    Entonces la API responde 201
    Y la respuesta trae un número de trámite
    Y el pedido queda en estado "EN_VALIDACION"

  Escenario: CA-01.2 Tipo de certificado no permitido
    Dado un estudiante con sesión iniciada
    Cuando pide un tipo de certificado que no existe
    Entonces la API responde 422
    Y no se guarda ningún pedido

  @E-07 @carga
  Escenario: CA-01.3 Temporada alta
    Dado que 500 estudiantes envían pedidos en 10 minutos
    Cuando la API los procesa
    Entonces el 95 % de las respuestas llega en menos de 2 segundos
    Y hay 0 pedidos perdidos
    Y los errores son menos del 1 %

  @E-06
  Escenario: CA-01.4 Sistema académico sin respuesta
    Dado un estudiante con sesión iniciada
    Y el sistema académico no responde
    Cuando pide un "certificado de matrícula"
    Entonces la API responde 201
    Y el pedido queda en estado "EN_VALIDACION" para validarse más tarde
```

### HU-02 · Consultar el estado de un pedido

```gherkin
# language: es
@HU-02
Característica: Consultar el estado de un pedido
  Como estudiante
  Quiero consultar el estado de mi pedido
  Para saber cuándo estará listo mi certificado

  Escenario: CA-02.1 Consulta de un pedido propio
    Dado un estudiante con un pedido registrado
    Cuando consulta ese pedido
    Entonces la API responde 200
    Y la respuesta muestra el estado del pedido

  @E-01 @E-04
  Escenario: CA-02.2 Intentos de ver pedidos ajenos
    Dado un estudiante A con sesión iniciada
    Y 200 pedidos que pertenecen a otros estudiantes
    Cuando el estudiante A intenta consultar cada uno de esos pedidos
    Entonces la API responde 404 en los 200 intentos, sin indicar si el pedido existe
    Y se devuelven 0 calificaciones
    Y los 200 intentos quedan guardados en la bitácora
```

### HU-03 · Aprobar o rechazar un pedido

```gherkin
# language: es
@HU-03
Característica: Resolver un pedido
  Como funcionario de Secretaría
  Quiero aprobar o rechazar un pedido
  Para que el certificado se emita una sola vez y solo cuando corresponde

  @E-04
  Escenario: CA-03.1 Aprobación de un pedido validado
    Dado un pedido en estado "VALIDADO"
    Cuando un funcionario lo aprueba
    Entonces la API responde 200
    Y el pedido queda en estado "APROBADO"
    Y se emite un solo certificado con código de verificación
    Y la aprobación queda en la bitácora con usuario, acción, recurso, fecha y hora, y dirección IP

  @E-02
  Escenario: CA-03.2 Aprobaciones simultáneas
    Dado 1 000 pedidos en estado "VALIDADO"
    Cuando dos funcionarios aprueban cada pedido al mismo tiempo
    Entonces hay 0 certificados duplicados
    Y en los 1 000 pares, la aprobación que llega segunda recibe 409 con el estado actual del pedido

  Escenario: CA-03.3 Rechazo con motivo
    Dado un pedido en estado "VALIDADO"
    Cuando un funcionario lo rechaza con el motivo "documentación incompleta"
    Entonces la API responde 200
    Y el pedido queda en estado "RECHAZADO"
    Y no se emite ningún certificado

  Escenario: CA-03.4 Un estudiante intenta aprobar
    Dado un estudiante con sesión iniciada
    Cuando intenta aprobar un pedido
    Entonces la API responde 403
    Y el pedido no cambia de estado

  Escenario: CA-03.5 Rechazo sin motivo
    Dado un pedido en estado "VALIDADO"
    Cuando un funcionario lo rechaza sin indicar el motivo
    Entonces la API responde 422
    Y el pedido no cambia de estado

  @E-06
  Escenario: CA-03.6 Sistema académico sin respuesta al aprobar
    Dado un pedido en estado "VALIDADO"
    Y el sistema académico no responde
    Cuando un funcionario lo aprueba
    Entonces la API responde 503
    Y el pedido sigue en estado "VALIDADO"
    Y no se emite ningún certificado
```

### HU-04 · Descargar el certificado

```gherkin
# language: es
@HU-04
Característica: Descargar el certificado
  Como estudiante
  Quiero descargar mi certificado en PDF
  Para presentarlo donde lo necesite

  @E-04
  Escenario: CA-04.1 Descarga de un certificado emitido
    Dado un estudiante con un pedido en estado "APROBADO"
    Cuando descarga el certificado
    Entonces la API responde 200 con un archivo PDF
    Y la descarga queda en la bitácora con sus cinco campos

  Escenario: CA-04.2 Pedido todavía sin aprobar
    Dado un estudiante con un pedido en estado "EN_VALIDACION"
    Cuando intenta descargar el certificado
    Entonces la API responde 409
    Y no se entrega ningún archivo

  @E-01 @E-04
  Escenario: CA-04.3 Certificado de otro estudiante
    Dado un estudiante A con sesión iniciada
    Y un certificado emitido para el estudiante B
    Cuando el estudiante A intenta descargarlo
    Entonces la API responde 404
    Y el intento queda guardado en la bitácora
```

### HU-05 · Verificar un certificado

```gherkin
# language: es
@HU-05
Característica: Verificar la autenticidad de un certificado
  Como entidad externa
  Quiero comprobar un certificado con su código
  Para saber si es auténtico sin llamar a la universidad

  @E-03
  Escenario: CA-05.1 Códigos reales
    Dado 100 certificados emitidos
    Cuando una entidad consulta cada código sin iniciar sesión
    Entonces la API responde 200 con "valido" en verdadero en los 100 casos
    Y muestra solo nombres, tipo de certificado y fecha de emisión, sin calificaciones

  @E-03
  Escenario: CA-05.2 Códigos alterados
    Dado 100 códigos de verificación con un carácter cambiado
    Cuando una entidad consulta cada código
    Entonces la API responde 200 con "valido" en falso en los 100 casos
    Y no muestra datos del estudiante
```

### Medida que verifica cada criterio

| Criterio | Escenario | Medida que verifica |
|---|---|---|
| CA-01.3 | E-07 | El 95 % de las respuestas en menos de 2 s con 500 pedidos en 10 min; 0 pedidos perdidos; menos del 1 % de errores. Lleva la etiqueta `@carga`: se ejecuta con una herramienta de carga en la semana 3 y no forma parte de las pruebas del esqueleto |
| CA-01.4 y CA-03.6 | E-06 | 0 pedidos perdidos durante la caída. Los reintentos cada 5 minutos (máximo 6) son extensión posterior: la tarea programada no entra en el esqueleto |
| CA-02.2 y CA-04.3 | E-01 | 100 % de 200 intentos rechazados; 0 calificaciones devueltas; 100 % de los intentos en la bitácora |
| CA-03.1 y CA-04.1 | E-04 | 100 % de las operaciones registradas con los cinco campos |
| CA-03.2 | E-02 | 0 certificados duplicados en 1 000 pares de aprobaciones simultáneas; 100 % de las segundas aprobaciones con 409 |
| CA-05.1 y CA-05.2 | E-03 | 100 % de 100 códigos alterados marcados como no válidos; 0 errores con 100 códigos reales |

Los criterios sin escenario de calidad (CA-01.1, CA-01.2, CA-02.1, CA-03.3, CA-03.4, CA-03.5 y CA-04.2) verifican la funcionalidad básica del driver D6.

## Paso 3 · Revisión con la lista de verificación (ISO/IEC/IEEE 29148)

| Atributo | Pregunta | HU-01 | HU-02 | HU-03 | HU-04 | HU-05 |
|---|---|---|---|---|---|---|
| Necesario | ¿Responde a un stakeholder o a un driver? | Sí: S1, D6 | Sí: S1, S4, D1 | Sí: S2, D2 | Sí: S1, S4, D1 | Sí: S5, D2 |
| No ambiguo | ¿Admite una sola interpretación? | Cumple tras fijar los tipos de certificado permitidos (catálogo de S3) | Cumple: "ajeno" = pedido de otro estudiante | Cumple tras definir los estados del pedido | Cumple: solo pedidos en `APROBADO` | Cumple tras fijar qué datos se muestran |
| Verificable | ¿Tiene un criterio que se pueda comprobar? | Sí: CA-01.1 a CA-01.3 | Sí: CA-02.2 con la medida de E-01 | Sí: CA-03.2 con la medida de E-02 | Sí: CA-04.1 a CA-04.3 | Sí: CA-05.1 y CA-05.2 con la medida de E-03 |
| Consistente | ¿Contradice otro requisito o decisión? | No: lee el sistema académico sin modificarlo (R2, ADR-002) | No: coherente con R1 | No: coherente con R3 y ADR-001 | No: coherente con R1 | No: coherente con R1 (datos mínimos) |
| Trazable | ¿Se rastrea hasta un escenario y un artefacto? | Sí: HU-01 → E-07 → `POST /api/v1/solicitudes` | Sí: HU-02 → E-01 → `GET /api/v1/solicitudes/{id}` | Sí: HU-03 → E-02 → `PATCH /api/v1/solicitudes/{id}/resolucion` | Sí: HU-04 → E-01 → `GET /api/v1/solicitudes/{id}/certificado` | Sí: HU-05 → E-03 → `GET /api/v1/verificaciones/{codigo}` |

## Paso 4 · Trazabilidad

| Historia | Escenario | Criterios | Endpoint | ADR | Issue en GitHub |
|---|---|---|---|---|---|
| HU-01 | E-07 (E-06 extensión) | CA-01.1 a CA-01.4 | `POST /api/v1/solicitudes` | ADR-002, ADR-003 | _(número al crear el issue)_ |
| HU-02 | E-01, E-04 | CA-02.1 y CA-02.2 | `GET /api/v1/solicitudes/{id}` | ADR-003 | |
| HU-03 | E-02, E-04, E-06 | CA-03.1 a CA-03.6 | `PATCH /api/v1/solicitudes/{id}/resolucion` | ADR-001, ADR-003 | |
| HU-04 | E-01, E-04 | CA-04.1 a CA-04.3 | `GET /api/v1/solicitudes/{id}/certificado` | ADR-003 | |
| HU-05 | E-03 | CA-05.1 y CA-05.2 | `GET /api/v1/verificaciones/{codigo}` | ADR-003 | |

E-05 (cambio de adaptador) y E-08 (instalación) no se verifican con criterios de usuario, porque no describen una acción del usuario final: E-05 se controla con las reglas de dependencia entre módulos (T08) y E-08 con la instalación desde cero en la integración continua.

## Contraste con IA

Las historias y los criterios partieron de un borrador generado con IA (ver `04-registro-ia.md`, fila 11). El borrador se revisó con la lista del Paso 3.

| Aspecto | Trabajo manual | Con IA | Observación |
|---|---|---|---|
| Esfuerzo | Más (estimado): redactar 5 historias y 15 criterios desde cero | Menos: el borrador salió completo en una sola respuesta | La revisión con la lista tomó más tiempo que generar el borrador |
| Defectos encontrados al revisar | — | 3 criterios sin la medida numérica de su escenario (pedidos ajenos, aprobaciones simultáneas y códigos alterados), CA-05.1 sin la cantidad de códigos reales y el estado `APROBADO` sin definir | Se corrigieron copiando la medida exacta del `01` |
| Cobertura de E-01 a E-08 | — | Cubría E-01 a E-04 y E-06; no tenía criterio para E-07 | Se agregó CA-01.3 para E-07 |

## Referencias

ISO/IEC/IEEE. (2018). *ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering*. International Organization for Standardization.

Smart, J. F. (2014). *BDD in action: Behavior-driven development for the whole software lifecycle*. Manning.
