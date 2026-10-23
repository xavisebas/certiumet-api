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
