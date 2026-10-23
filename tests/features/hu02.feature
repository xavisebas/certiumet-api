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
