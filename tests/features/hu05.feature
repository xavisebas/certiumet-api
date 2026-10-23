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
