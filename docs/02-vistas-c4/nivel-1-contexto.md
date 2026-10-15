# Vista C4 · Nivel 1: Contexto del sistema

**Para quién es:** Secretaría General, jefatura, delegado de protección de datos y cualquier persona no técnica.
**Qué muestra:** el sistema CertiUMET como una sola caja, las personas que lo usan y los sistemas externos con los que se comunica. En este nivel no se nombran tecnologías (Brown, s. f.).
**Decisiones que refleja:** ADR-002 (el sistema académico solo se lee) y ADR-003 (CertiUMET es un solo sistema).

```mermaid
flowchart TB
    EXT["👤 Entidad verificadora externa<br/><i>Persona</i><br/>Empleador u otra universidad"]
    DPD["👤 Delegado de protección de datos<br/><i>Persona</i><br/>Revisa quién accedió a cada dato"]
    EST["👤 Estudiante<br/><i>Persona</i><br/>Pide y descarga sus certificados"]
    FUN["👤 Funcionario de Secretaría<br/><i>Persona</i><br/>Revisa y resuelve los pedidos"]
    JEF["👤 Jefatura de Secretaría General<br/><i>Persona</i><br/>Define tipos de certificado y plazos"]

    SIS["<b>CertiUMET</b><br/><i>Sistema de software</i><br/>Recibe pedidos de certificados, los valida,<br/>emite el certificado y permite verificarlo"]

    IDP["Sistema de usuarios institucional<br/><i>Sistema externo</i><br/>Inicio de sesión de estudiantes y funcionarios"]
    ACA["Sistema académico institucional<br/><i>Sistema externo</i><br/>Fuente oficial de datos y calificaciones"]
    COR["Correo institucional<br/><i>Sistema externo</i><br/>Entrega los avisos por correo"]

    EXT -- "Verifica un certificado con su código" --> SIS
    DPD -- "Consulta la bitácora de accesos" --> SIS
    EST -- "Pide, consulta y descarga certificados" --> SIS
    FUN -- "Aprueba o rechaza pedidos" --> SIS
    JEF -- "Configura tipos y revisa indicadores" --> SIS

    SIS -- "Valida la sesión del usuario" --> IDP
    SIS -- "Lee datos del estudiante y calificaciones (solo lectura)" --> ACA
    SIS -- "Envía al estudiante los avisos de cambio de estado" --> COR

    classDef persona fill:#08427b,stroke:#052e56,color:#ffffff
    classDef sistema fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef externo fill:#8a8a8a,stroke:#5e5e5e,color:#ffffff
    class EST,FUN,JEF,DPD,EXT persona
    class SIS sistema
    class IDP,ACA,COR externo
```

## Elementos del diagrama

| Elemento | Tipo | Responsabilidad | Stakeholder o restricción |
|---|---|---|---|
| Estudiante | Persona | Pide certificados, revisa el estado y descarga el PDF | S1 |
| Funcionario de Secretaría | Persona | Revisa los datos y aprueba o rechaza cada pedido | S2 |
| Jefatura de Secretaría General | Persona | Define tipos de certificado y plazos, y revisa indicadores | S3 |
| Delegado de protección de datos | Persona | Revisa la bitácora de accesos a datos personales | S4, R1 |
| Entidad verificadora externa | Persona | Comprueba si un certificado es auténtico | S5 |
| CertiUMET | Sistema de software | Gestiona el pedido, la emisión y la verificación de certificados | Todo el caso |
| Sistema de usuarios institucional | Sistema externo | Confirma la identidad de quien inicia sesión | A2 |
| Sistema académico institucional | Sistema externo | Entrega los datos y calificaciones oficiales; CertiUMET solo los lee | S6, R2, A1 |
| Correo institucional | Sistema externo | Hace llegar los avisos al estudiante | R6 |

## Relación con los escenarios de calidad

| Escenario | Dónde se ve en este nivel |
|---|---|
| EC-01, EC-04 | El delegado de protección de datos consulta la bitácora; solo personas autenticadas acceden a datos personales |
| EC-03 | La entidad externa verifica certificados sin iniciar sesión y sin acceso a calificaciones |
| EC-05, EC-06 | La comunicación con el sistema académico es de solo lectura y pasa por un único punto |

## Referencias

Brown, S. (s. f.). *The C4 model for visualising software architecture*. https://c4model.com
