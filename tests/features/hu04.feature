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
