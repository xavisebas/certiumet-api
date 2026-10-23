# Revisión del contrato OpenAPI — API CertiUMET

- **Archivo revisado:** `api/pruebas/openapi-con-defectos.yaml` (versión 0.2.0)
- **Especificación:** OpenAPI 3.0.3
- **Requisitos de referencia:** HU-01 a HU-05 y R1 (Ley Orgánica de Protección de Datos Personales)
- **Fecha de revisión:** 23 de octubre de 2026
- **Defectos encontrados:** 11

---

## 1. Tabla resumen

| N.º | Ubicación | Defecto (resumen) | Tipo | Requisito |
|:---:|---|---|---|---|
| 1 | `paths./api/v1/verificaciones/{codigo}.get` | Hereda la seguridad global y exige token | Significado | HU-05 |
| 2 | `paths./api/v1/solicitudes/{id}.get.tags` | Etiqueta `Pedidos` no declarada | Estructura | HU-02 |
| 3 | `paths./api/v1/solicitudes/{id}.get` | Falta `operationId` | Estructura | HU-02 |
| 4 | `paths./api/v1/solicitudes/{id}/resolucion.patch.responses` | Falta la respuesta `409` | Significado | HU-03 (E-02) |
| 5 | `components.schemas.Resolucion.motivo` | Obligatoriedad del motivo solo en texto | Significado | HU-03 |
| 6 | `paths./api/v1/solicitudes/{id}/certificado.get.parameters` | Parámetro `idSolicitud` no coincide con `{id}` | Estructura | HU-04 |
| 7 | `components.schemas.NuevaSolicitud` | Exige la cédula del estudiante | Significado | R1, HU-01 |
| 8 | `components.schemas.Solicitud.fechaCreacion.example` | Ejemplo numérico en un campo `date-time` | Estructura | HU-01, HU-02 |
| 9 | `components.schemas.Verificacion` | No impide campos adicionales (calificaciones) | Significado | HU-05 (E-03), R1 |
| 10 | `components.schemas.Verificacion` | Datos del titular no condicionados a `valido: true` | Significado | HU-05, R1 |
| 11 | `info.license.url` | La URL no apunta a una licencia | Estructura (menor) | — |

---

## 2. Detalle de cada defecto

### Defecto 1 — La verificación pública exige token

- **Ubicación:** `security` (raíz) + `paths./api/v1/verificaciones/{codigo}.get`
- **Tipo:** Significado
- **Requisito afectado:** HU-05
- **Defecto:** La seguridad global `tokenUsuario` se aplica a todas las operaciones. La operación `verificarCertificado` no la anula, por lo que exige token. Esto contradice su propia descripción ("acceso público sin iniciar sesión").
- **Corrección propuesta:**

```yaml
  /api/v1/verificaciones/{codigo}:
    get:
      tags: [Verificaciones]
      operationId: verificarCertificado
      security: []
```

---

### Defecto 2 — Etiqueta no declarada

- **Ubicación:** `paths./api/v1/solicitudes/{id}.get.tags`
- **Tipo:** Estructura
- **Requisito afectado:** HU-02
- **Defecto:** Usa la etiqueta `Pedidos`, que no está declarada en `tags`. Las demás operaciones de pedidos usan `Solicitudes`, así que esta operación queda agrupada aparte en la documentación.
- **Corrección propuesta:**

```yaml
      tags: [Solicitudes]
```

---

### Defecto 3 — Falta `operationId`

- **Ubicación:** `paths./api/v1/solicitudes/{id}.get`
- **Tipo:** Estructura
- **Requisito afectado:** HU-02
- **Defecto:** Es la única operación sin `operationId`. Sin él, el código generado y las referencias quedan con nombres arbitrarios.
- **Corrección propuesta:**

```yaml
      operationId: consultarSolicitud
```

---

### Defecto 4 — Falta la respuesta 409 en la resolución

- **Ubicación:** `paths./api/v1/solicitudes/{id}/resolucion.patch.responses`
- **Tipo:** Significado
- **Requisito afectado:** HU-03 (escenario E-02, ADR-001)
- **Defecto:** La descripción dice que una segunda aprobación recibe 409 con el estado actual, pero `responses` no lo declara. El componente `Conflicto` existe, pero solo se usa en la descarga.
- **Corrección propuesta:**

```yaml
        "409":
          $ref: "#/components/responses/Conflicto"
```

---

### Defecto 5 — El motivo de rechazo no es obligatorio en el esquema

- **Ubicación:** `components.schemas.Resolucion.motivo`
- **Tipo:** Significado
- **Requisito afectado:** HU-03
- **Defecto:** La regla "obligatorio cuando la decisión es RECHAZAR" está solo en `description`. El esquema acepta `{"decision": "RECHAZAR"}` sin motivo.
- **Corrección propuesta:**

```yaml
    Resolucion:
      oneOf:
        - type: object
          required: [decision]
          additionalProperties: false
          properties:
            decision:
              type: string
              enum: [APROBAR]
        - type: object
          required: [decision, motivo]
          additionalProperties: false
          properties:
            decision:
              type: string
              enum: [RECHAZAR]
            motivo:
              type: string
              minLength: 1
              maxLength: 300
```

---

### Defecto 6 — El parámetro de ruta no coincide con la plantilla

- **Ubicación:** `paths./api/v1/solicitudes/{id}/certificado.get.parameters`
- **Tipo:** Estructura
- **Requisito afectado:** HU-04
- **Defecto:** El parámetro se llama `idSolicitud`, pero la ruta usa `{id}`. La plantilla queda sin parámetro definido y el parámetro declarado no existe en la ruta, lo que **hace inválido el documento**. Además le falta `minimum: 1`, a diferencia del resto.
- **Corrección propuesta:**

```yaml
      parameters:
        - $ref: "#/components/parameters/IdSolicitud"
```

---

### Defecto 7 — Se pide la cédula del estudiante

- **Ubicación:** `components.schemas.NuevaSolicitud` (`required` y `properties.cedula`)
- **Tipo:** Significado
- **Requisito afectado:** R1, HU-01
- **Defecto:** Exige la cédula en el cuerpo del pedido. Es un dato personal innecesario, porque el estudiante ya se identifica por su token, y contradice `info.description`. Como consecuencia, el `example` del POST (`tipoCertificado: MATRICULA`) no cumple el esquema.
- **Corrección propuesta:**

```yaml
    NuevaSolicitud:
      type: object
      required: [tipoCertificado]
      additionalProperties: false
      properties:
        tipoCertificado:
          $ref: "#/components/schemas/TipoCertificado"
```

---

### Defecto 8 — Ejemplo de fecha con tipo incorrecto

- **Ubicación:** `components.schemas.Solicitud.fechaCreacion.example`
- **Tipo:** Estructura
- **Requisito afectado:** HU-01, HU-02
- **Defecto:** El ejemplo `20261020` es un número entero, pero el campo es `string` con `format: date-time`.
- **Corrección propuesta:**

```yaml
        fechaCreacion:
          type: string
          format: date-time
          example: "2026-10-20T10:15:00-05:00"
```

---

### Defecto 9 — La verificación no impide exponer campos adicionales

- **Ubicación:** `components.schemas.Verificacion`
- **Tipo:** Significado
- **Requisito afectado:** HU-05 (E-03), R1
- **Defecto:** Sin `additionalProperties: false`, la respuesta podría incluir otros campos, como calificaciones. La restricción "nunca calificaciones" solo está escrita en el texto.
- **Corrección propuesta:** agregar `additionalProperties: false` al esquema (ver la versión completa en el defecto 10).

---

### Defecto 10 — Los datos del titular no dependen de que el código sea válido

- **Ubicación:** `components.schemas.Verificacion` (`nombres`, `tipoCertificado`, `fechaEmision`)
- **Tipo:** Significado
- **Requisito afectado:** HU-05, R1
- **Defecto:** La descripción dice que esos datos aparecen "solo si el código es válido", pero el esquema permite enviarlos también con `valido: false`.
- **Corrección propuesta (incluye el defecto 9):**

```yaml
    Verificacion:
      oneOf:
        - type: object
          required: [valido, nombres, tipoCertificado, fechaEmision]
          additionalProperties: false
          properties:
            valido:
              type: boolean
              enum: [true]
            nombres:
              type: string
            tipoCertificado:
              $ref: "#/components/schemas/TipoCertificado"
            fechaEmision:
              type: string
              format: date
        - type: object
          required: [valido]
          additionalProperties: false
          properties:
            valido:
              type: boolean
              enum: [false]
```

---

### Defecto 11 — La URL de licencia no apunta a una licencia

- **Ubicación:** `info.license.url`
- **Tipo:** Estructura (menor)
- **Requisito afectado:** —
- **Defecto:** Apunta al repositorio y no al texto de la licencia.
- **Corrección propuesta:**

```yaml
  license:
    name: Uso académico
    url: https://github.com/xavisebas/certiumet-api/blob/main/LICENSE
```

Si el repositorio no tiene archivo de licencia, retirar `url`.

---

## 3. Clasificación por gravedad

| Grupo | Defectos | Comentario |
|---|---|---|
| Inválido según OpenAPI 3.0.3 | 6 | Es el único que hace inválido el documento. |
| Ejemplos que no cumplen su esquema | 7, 8 | La especificación indica que los ejemplos deben ajustarse al esquema, pero no invalidan el documento. |
| Consistencia y documentación | 2, 3, 11 | Declarar todas las etiquetas y usar `operationId` es opcional en 3.0.3; son defectos de calidad. |
| Incumplimiento de requisitos | 1, 4, 5, 7, 9, 10 | Los más graves para el caso: el contrato es válido pero no dice lo que los requisitos exigen. |
