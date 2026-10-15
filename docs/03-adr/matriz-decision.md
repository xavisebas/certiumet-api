# Matriz ponderada de decisión · Estilo arquitectónico

**Decisión que apoya:** ADR-003 (estilo arquitectónico)
**Fecha:** 14/10/2026

## 1. Alternativas comparadas

| ID | Alternativa | Descripción breve |
|---|---|---|
| A | **Monolito modular con arquitectura hexagonal** | Un solo proyecto Django que se despliega como una unidad. Por dentro se divide en módulos (solicitudes, emisión y verificación, auditoría, conexión académica y notificaciones). La lógica de negocio solo conoce puertos, y los detalles técnicos (base de datos, sistema académico, correo) van en adaptadores. Usa una sola base PostgreSQL. |
| B | **Microservicios** | Cuatro servicios independientes (solicitudes, emisión y verificación, auditoría, conexión académica), cada uno con su propia base de datos, comunicados por HTTP y eventos, con un API Gateway al frente. |
| C | **Monolito en capas tradicional** | Un proyecto Django con la estructura habitual (modelos, vistas y serializadores). Las vistas consultan directo al sistema académico y la lógica de negocio queda repartida en vistas y modelos. Usa una sola base PostgreSQL. |

## 2. Criterios y pesos

Los criterios son los escenarios de calidad del documento `01-contexto-y-drivers.md`. El escenario de funcionalidad básica (D6) no se incluye porque las tres alternativas lo cumplen por igual. El peso de cada escenario sale de su prioridad:

| Prioridad | Escenarios | Peso de cada uno | Subtotal |
|---|---|---|---|
| 1 | EC-01, EC-02 | 17 % | 34 % |
| 2 | EC-03, EC-04, EC-05 | 13 % | 39 % |
| 3 | EC-06, EC-07 | 10 % | 20 % |
| 4 | EC-08 | 7 % | 7 % |
| | | **Total** | **100 %** |

**Escala de calificación:** 1 = no permite cumplir la medida del escenario; 3 = la cumple con trabajo o riesgo adicional; 5 = la cumple de forma directa.

## 3. Matriz

| Escenario | Peso | A · Monolito modular hexagonal | B · Microservicios | C · Monolito en capas |
|---|---|---|---|---|
| EC-01 Confidencialidad | 17 % | 4 | 3 | 4 |
| EC-02 Integridad | 17 % | 5 | 2 | 5 |
| EC-03 Autenticidad | 13 % | 4 | 4 | 4 |
| EC-04 Responsabilidad | 13 % | 5 | 3 | 3 |
| EC-05 Modificabilidad | 13 % | 5 | 4 | 2 |
| EC-06 Tolerancia a fallos | 10 % | 4 | 5 | 2 |
| EC-07 Desempeño | 10 % | 4 | 5 | 4 |
| EC-08 Instalabilidad | 7 % | 5 | 2 | 5 |
| **Puntaje ponderado (sobre 5)** | **100 %** | **4,50** | **3,42** | **3,65** |

Cálculo: puntaje = Σ (peso × calificación). Por ejemplo, para A: 0,17·4 + 0,17·5 + 0,13·4 + 0,13·5 + 0,13·5 + 0,10·4 + 0,10·4 + 0,07·5 = 4,50.

## 4. Justificación de las calificaciones

| Escenario | A · Monolito modular hexagonal | B · Microservicios | C · Monolito en capas |
|---|---|---|---|
| EC-01 | El control de acceso por dueño se programa una sola vez en la capa de aplicación (4) | Cada servicio debe validar el token y el dueño del pedido; hay más puntos donde puede fallar (3) | Usa el mismo control de Django, pero repartido en cada vista (4) |
| EC-02 | Una transacción local con bloqueo de fila y `UNIQUE` en la misma base (5) | Pedido y certificado viven en bases distintas; evitar duplicados exige coordinar servicios (sagas o idempotencia), lo que es más difícil y más riesgoso (2) | Igual que A: una sola base y una transacción local (5) |
| EC-03 | Código de verificación firmado en el módulo de emisión (4) | Igual mecanismo en el servicio de emisión (4) | Igual mecanismo (4) |
| EC-04 | La bitácora se guarda en la misma transacción que la operación, desde un solo punto (5) | La bitácora es otro servicio y recibe eventos; si el evento se pierde, el registro queda incompleto (3) | Se puede registrar, pero depende de recordar hacerlo en cada vista (3) |
| EC-05 | Solo se cambia el adaptador académico (5) | El servicio de conexión académica se cambia solo, pero hay que cuidar el contrato con los demás servicios (4) | La consulta al sistema académico está dentro de las vistas; hay que modificar varias partes (2) |
| EC-06 | El adaptador maneja el tiempo de espera y la tarea de reintentos; el resto del sistema sigue funcionando (4) | La caída afecta solo al servicio de conexión académica (5) | El pedido falla si el sistema académico no responde (2) |
| EC-07 | 500 pedidos en 10 minutos se atienden con varios procesos de Gunicorn en un solo contenedor (4) | Cada servicio escala por separado (5) | Igual que A en capacidad (4) |
| EC-08 | Un solo `docker-compose.yml` con una API, su tarea programada, una base de datos y los servicios simulados (5) | Cuatro servicios, cuatro bases, gateway y mensajería: más contenedores y más configuración (2) | Igual que A (5) |

## 5. Trade-off explícito

La alternativa A gana con **4,50**, pero no gana en todo:

- **A frente a B:** A pierde en **EC-06** (4 contra 5) y en **EC-07** (4 contra 5), porque los microservicios aíslan mejor las caídas y escalan por partes. Esta pérdida se acepta porque el volumen esperado es bajo (A3: picos de 500 pedidos por hora) y el equipo es de una sola persona (R5); mantener cuatro servicios con sus bases no se justifica para este tamaño. A cambio, A protege mejor los dos escenarios de mayor prioridad: **EC-02** (5 contra 2) y **EC-04** (5 contra 3).
- **A frente a C:** A cuesta más trabajo al inicio, porque hay que programar puertos y adaptadores. Esta inversión se acepta porque mejora **EC-05** (5 contra 2) y **EC-06** (4 contra 2), que son justamente los que permiten pasar del servicio simulado al sistema académico real.

## 6. Prueba de sensibilidad

Para revisar si el resultado depende demasiado de los pesos, se duplicó el peso de EC-06 y EC-07 (de 10 % a 20 % cada uno, que son los escenarios donde B es mejor) y se volvieron a calcular los puntajes:

| Alternativa | Puntaje original | Puntaje con EC-06 y EC-07 duplicados |
|---|---|---|
| A · Monolito modular hexagonal | 4,50 | 4,42 |
| B · Microservicios | 3,42 | 3,68 |
| C · Monolito en capas | 3,65 | 3,54 |

A sigue en primer lugar, así que la decisión se mantiene aunque el desempeño y la tolerancia a fallos tuvieran más peso.
