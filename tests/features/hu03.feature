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
