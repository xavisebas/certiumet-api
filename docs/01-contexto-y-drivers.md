# 01 · Contexto y drivers arquitectónicos

**Proyecto:** CertiUMET API: solicitud y emisión de certificados académicos
**Caso:** Secretaría General de la Universidad Metropolitana del Ecuador (UMET)
**Módulo:** M8 · Automatización de Procesos de Software, Unidad 1
**Hito:** H1 · Dossier de arquitectura (`v0.1.0`)
**Modalidad:** trabajo individual

---

## 1. Descripción del caso

La Secretaría General de la UMET entrega certificados académicos a los estudiantes: certificado de matrícula, récord de calificaciones y certificado de culminación de estudios. Hoy el trámite se hace en ventanilla o por correo. El funcionario recibe el pedido, busca los datos del estudiante en el sistema académico de la universidad (base de datos Oracle, esquema `sna`), arma el documento y se lo entrega al estudiante.

Este proceso tiene cuatro problemas claros:

1. **El estudiante no sabe en qué va su trámite.** No hay seguimiento, así que debe volver a preguntar en ventanilla o por correo.
2. **Hay días de mucha demanda.** Es común que al cierre de cada período académico y en la temporada de graduaciones lleguen muchos pedidos en pocos días.
3. **Las calificaciones viajan por correo sin control.** No queda registro de quién las vio ni de quién las envió.
4. **Nadie puede comprobar si un certificado es real.** Un empleador o una universidad que recibe el documento no tiene cómo verificarlo sin llamar a la Secretaría.

Por eso se plantea construir una **API REST** para pedir, consultar, aprobar y verificar certificados. La API solo lee datos del sistema académico, nunca los cambia, y guarda un registro de cada acceso a datos personales.

### 1.1 Alcance funcional

| Código | Endpoint | Qué hace | Quién lo usa |
|---|---|---|---|
| CU-01 | `POST /api/v1/solicitudes` | Registra un pedido de certificado | Estudiante |
| CU-02 | `GET /api/v1/solicitudes/{id}` | Muestra el estado de un pedido propio | Estudiante |
| CU-03 | `PATCH /api/v1/solicitudes/{id}/resolucion` | Aprueba o rechaza el pedido; al aprobar se emite el certificado | Funcionario de Secretaría |
| CU-04 | `GET /api/v1/solicitudes/{id}/certificado` | Descarga el certificado en PDF | Estudiante |
| CU-05 | `GET /api/v1/verificaciones/{codigo}` | Indica si un certificado es auténtico a partir de su código | Entidad externa |

### 1.2 Partes del sistema y sistemas externos

- **Gestión de solicitudes y emisión:** controla el recorrido de cada pedido (`REGISTRADA → EN_VALIDACION → APROBADA o RECHAZADA → EMITIDA`).
- **Bitácora de auditoría:** guarda quién hizo qué con los datos personales y cuándo.
- **Conexión con el sistema académico:** trae los datos del estudiante y sus calificaciones. En el proyecto se **simula** con un servicio de datos ficticios; en un caso real sería el sistema académico de la universidad (Oracle).
- **Notificaciones:** envía un correo institucional cuando cambia el estado del pedido.
- **Base de datos propia:** PostgreSQL.

---

## 2. Stakeholders y concerns

La norma ISO/IEC/IEEE 42010 pide describir a cada interesado (stakeholder) por sus intereses o preocupaciones, llamados *concerns* (ISO/IEC/IEEE, 2022). Por eso los concerns se escriben como necesidades de cada persona y no como soluciones técnicas.

| ID | Stakeholder | Qué hace en el sistema | Concerns | Influencia |
|---|---|---|---|---|
| S1 | Estudiante | Pide y descarga certificados | Obtener el certificado sin ir a ventanilla; saber en todo momento cómo va su trámite; que sus calificaciones solo las vea personal autorizado | Alta |
| S2 | Funcionario de Secretaría | Revisa y resuelve los pedidos | Contar con datos académicos confiables para revisar; no emitir dos veces el mismo certificado; atender todos los pedidos en temporada alta | Alta |
| S3 | Secretaría General (jefatura) | Define los tipos de certificado y los plazos | Cumplir los plazos de atención; saber cuántos pedidos se atienden; respaldar cada documento que se emite | Media |
| S4 | Delegado de protección de datos | Controla que se cumpla la ley | Que los datos personales se usen solo para lo necesario; saber quién vio cada dato y cuándo | Alta |
| S5 | Entidad externa (empleador u otra universidad) | Revisa certificados que recibe | Saber rápido si un certificado es auténtico, sin tener que llamar a la Secretaría | Media |
| S6 | Dirección de TI (dueña del sistema académico) | Administra la fuente oficial de datos | Que el sistema académico no se vuelva lento por consultas de otros sistemas; que ningún sistema externo cambie datos académicos | Alta |
| S7 | Desarrollador (equipo de una persona) | Construye y mantiene la API | Poder cambiar una parte sin rehacer todo; desplegar de forma sencilla y siempre igual; trabajar con bajo costo | Media |

---

## 3. Restricciones y supuestos

### 3.1 Restricciones

| ID | Restricción | Origen | Negociable |
|---|---|---|---|
| R1 | Cumplir la Ley Orgánica de Protección de Datos Personales (Asamblea Nacional del Ecuador, 2021): usar solo los datos necesarios, para un fin claro y protegidos | Legal | No |
| R2 | El sistema académico es la **única fuente oficial** de calificaciones; la API solo puede leerlo, nunca modificarlo | Organizacional (Dirección de TI) | No |
| R3 | Un pedido no puede generar dos certificados | Regla de negocio (Secretaría) | No |
| R4 | Usar software libre, sin licencias de pago (Python, Django REST Framework, PostgreSQL) | Económica | Parcial |
| R5 | Equipo de una sola persona y plazo de cuatro semanas, que es lo que dura el módulo | Organizacional y académica | No |
| R6 | Notificar solo por correo institucional; los mensajes de texto (SMS) quedan fuera | Económica | Parcial |
| R7 | Desplegar en Linux con contenedores y versionar en GitHub, listo para integración continua | Académica (módulo) | No |

### 3.2 Supuestos

| ID | Supuesto |
|---|---|
| A1 | En un caso real, el sistema académico ofrece una vista o un servicio de solo lectura. En el proyecto se reemplaza por un servicio simulado con datos ficticios. |
| A2 | El inicio de sesión de estudiantes y funcionarios lo maneja el sistema de usuarios de la universidad. En el proyecto se simula con tokens JWT. |
| A3 | Se considera una población de 10 000 estudiantes, con picos de hasta 500 pedidos por hora al cierre del período académico. |
| A4 | No se usan datos personales reales en el repositorio ni en herramientas de IA. Todos los datos de prueba son ficticios. |

---

## 4. Drivers arquitectónicos priorizados

Los drivers salen de los concerns y de las restricciones. Según Bass et al. (2021), se ordenan por su **importancia** para el negocio y por la **dificultad** de lograrlos con la arquitectura. Los que son altos en las dos cosas son los que más pesan al elegir el estilo arquitectónico.

| ID | Driver | Origen | Atributo de calidad (ISO/IEC 25010:2023) | Importancia | Dificultad |
|---|---|---|---|---|---|
| D1 | Proteger las calificaciones y registrar cada acceso a ellas | S1, S4, R1 | Seguridad (confidencialidad y responsabilidad) | Alta | Alta |
| D2 | Que cada certificado sea único, correcto y comprobable por terceros | S2, S5, R3 | Seguridad (integridad y autenticidad) | Alta | Alta |
| D3 | Conectarse al sistema académico de forma que se pueda cambiar (de simulado a Oracle) y sin afectarlo | S6, R2, A1 | Mantenibilidad (modificabilidad) y fiabilidad (tolerancia a fallos) | Alta | Media |
| D4 | Atender los picos de pedidos al cierre del período académico | S1, S2, A3 | Eficiencia de desempeño (comportamiento temporal) | Media | Media |
| D5 | Desplegar de forma sencilla, repetible y de bajo costo | S7, R4, R5, R7 | Flexibilidad (instalabilidad) | Media | Baja |
| D6 | Pedir, consultar, resolver y descargar certificados | S1, S2 | Adecuación funcional | Alta | Baja |

> **Sobre D6.** Se incluye porque es la razón de ser del sistema, pero casi no influye en la arquitectura: cualquier estilo (monolito, capas, hexagonal o microservicios) puede cumplirla. Por eso es preferible no usarla para comparar alternativas en la matriz de decisión (`03-adr`).

**Orden de prioridad:** D1 = D2 > D3 > D4 > D5 > D6.

---

## 5. Escenarios de calidad

Cada escenario tiene sus seis partes (fuente, estímulo, entorno, artefacto, respuesta y medida), revisa **un solo atributo de calidad** y tiene una **medida con números** que se puede comprobar con pruebas automáticas (Bass et al., 2021). Estas medidas serán, por ejemplo, los criterios que deberán pasar las pruebas del pipeline de integración continua en el hito H4.

### Resumen y prioridad

| ID | Atributo de calidad | Driver | Importancia | Dificultad | Prioridad |
|---|---|---|---|---|---|
| EC-01 | Seguridad · Confidencialidad | D1 | Alta | Alta | 1 |
| EC-02 | Seguridad · Integridad | D2 | Alta | Alta | 1 |
| EC-03 | Seguridad · Autenticidad | D2 | Alta | Media | 2 |
| EC-04 | Seguridad · Responsabilidad | D1 | Alta | Media | 2 |
| EC-05 | Mantenibilidad · Modificabilidad | D3 | Alta | Media | 2 |
| EC-06 | Fiabilidad · Tolerancia a fallos | D3 | Media | Media | 3 |
| EC-07 | Eficiencia de desempeño · Comportamiento temporal | D4 | Media | Media | 3 |
| EC-08 | Flexibilidad · Instalabilidad | D5 | Media | Baja | 4 |

### EC-01 · Confidencialidad de las calificaciones (D1)

| Parte | Descripción |
|---|---|
| Fuente | Estudiante A con sesión iniciada |
| Estímulo | Cambia el `{id}` de la URL para ver el pedido o el certificado del estudiante B |
| Entorno | Funcionamiento normal |
| Artefacto | Endpoints CU-02 y CU-04 (control de acceso por dueño del pedido) |
| Respuesta | La API responde `404 Not Found`, sin decir si el pedido existe, y guarda el intento en la bitácora |
| Medida | 100 % de 200 intentos de acceso a pedidos ajenos rechazados en la prueba automática; 0 calificaciones devueltas; 100 % de los intentos guardados en la bitácora |

### EC-02 · Integridad: un pedido, un solo certificado (D2)

| Parte | Descripción |
|---|---|
| Fuente | Dos funcionarios de Secretaría |
| Estímulo | Aprueban el mismo pedido al mismo tiempo |
| Entorno | Temporada alta (cierre del período académico) |
| Artefacto | Servicio de resolución y emisión (CU-03) |
| Respuesta | Solo una de las aprobaciones genera el certificado; la otra recibe `409 Conflict` con el estado actual del pedido |
| Medida | 0 certificados duplicados en 1 000 pares de aprobaciones simultáneas; 100 % de las aprobaciones que llegan segundas reciben `409 Conflict` |

### EC-03 · Autenticidad del certificado (D2)

| Parte | Descripción |
|---|---|
| Fuente | Entidad externa (empleador u otra universidad) |
| Estímulo | Consulta un código de verificación, que puede ser real o alterado |
| Entorno | Funcionamiento normal, acceso público sin iniciar sesión |
| Artefacto | Endpoint de verificación (CU-05) |
| Respuesta | Indica si el certificado es válido y muestra solo lo mínimo (nombres, tipo de certificado y fecha de emisión), sin calificaciones |
| Medida | 100 % de 100 códigos alterados marcados como no válidos; 0 errores con 100 códigos reales (todos confirmados como auténticos) |

### EC-04 · Responsabilidad: registro de accesos (D1)

| Parte | Descripción |
|---|---|
| Fuente | Funcionario de Secretaría |
| Estímulo | Consulta los datos académicos de un estudiante, resuelve un pedido o descarga un certificado |
| Entorno | Funcionamiento normal |
| Artefacto | Bitácora de auditoría |
| Respuesta | Se guarda el usuario, la acción, el recurso, la fecha y hora, y la dirección IP; la bitácora no se puede editar ni borrar desde la API |
| Medida | 100 % de las operaciones sobre datos personales registradas durante las pruebas; 0 ediciones o borrados permitidos en la bitácora; 100 % de los registros con los cinco campos completos |

### EC-05 · Modificabilidad: cambiar la conexión al sistema académico (D3)

| Parte | Descripción |
|---|---|
| Fuente | Dirección de TI |
| Estímulo | Pide cambiar el servicio académico simulado por la conexión real al sistema académico de la universidad |
| Entorno | Etapa de desarrollo |
| Artefacto | Módulo de conexión con el sistema académico |
| Respuesta | El cambio se hace reemplazando solo el adaptador de conexión, sin tocar las reglas de negocio ni la forma de los endpoints |
| Medida | Como máximo 1 módulo modificado; 0 cambios en los endpoints CU-01 a CU-05; 100 % de las pruebas existentes aprobadas después del cambio; 8 horas de trabajo o menos |

### EC-06 · Tolerancia a fallos del sistema académico (D3)

| Parte | Descripción |
|---|---|
| Fuente | Sistema académico |
| Estímulo | Deja de responder durante 30 minutos |
| Entorno | Funcionamiento normal, con pedidos en curso |
| Artefacto | Módulo de conexión con el sistema académico y gestión de solicitudes |
| Respuesta | Los pedidos nuevos quedan en estado `EN_VALIDACION` y se vuelven a validar solos más tarde; la consulta de estado (CU-02) sigue funcionando |
| Medida | 0 pedidos perdidos; consulta de estado disponible el 100 % del tiempo de la caída; reintentos cada 5 minutos (máximo 6) y validación completa en menos de 10 minutos después de que el sistema académico vuelve |

### EC-07 · Desempeño en temporada alta (D4)

| Parte | Descripción |
|---|---|
| Fuente | Estudiantes |
| Estímulo | Envían 500 pedidos en 10 minutos |
| Entorno | Cierre del período académico |
| Artefacto | Endpoint de registro de pedidos (CU-01) |
| Respuesta | Todos los pedidos se registran y cada estudiante recibe su número de trámite |
| Medida | El 95 % de las respuestas en menos de 2 segundos; 0 pedidos perdidos; menos del 1 % de errores en la prueba de carga |

### EC-08 · Instalabilidad del entorno (D5)

| Parte | Descripción |
|---|---|
| Fuente | Desarrollador o evaluador del proyecto |
| Estímulo | Instala la API desde cero a partir del repositorio |
| Entorno | Equipo con Linux (o WSL2) y Docker instalado |
| Artefacto | Archivos de despliegue (`docker-compose.yml`) y documentación del repositorio |
| Respuesta | Quedan funcionando la API (con su tarea programada), la base de datos PostgreSQL, el servicio académico simulado y el servidor de correo de pruebas |
| Medida | Entorno funcionando con 1 comando en menos de 10 minutos; 0 pasos manuales fuera de los que indica el `README.md` |

---

## 6. Trazabilidad

La siguiente tabla une cada stakeholder o restricción con su driver y sus escenarios. Esto ayuda a comprobar que ninguna preocupación importante quedó sin un escenario que la mida.

| Stakeholder o restricción | Driver | Escenarios |
|---|---|---|
| S1, S4, R1 | D1 | EC-01, EC-04 |
| S2, S5, R3 | D2 | EC-02, EC-03 |
| S6, R2, A1 | D3 | EC-05, EC-06 |
| S1, S2, A3 | D4 | EC-07 |
| S7, R4, R5, R7 | D5 | EC-08 |

---

## Referencias

Asamblea Nacional del Ecuador. (2021). *Ley Orgánica de Protección de Datos Personales* (Registro Oficial Suplemento 459, 26 de mayo de 2021).

Bass, L., Clements, P., & Kazman, R. (2021). *Software architecture in practice* (4.ª ed.). Addison-Wesley.

ISO/IEC. (2023). *ISO/IEC 25010:2023 Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. International Organization for Standardization.

ISO/IEC/IEEE. (2022). *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*. International Organization for Standardization.
