from django.db import models


class Certificado(models.Model):
    # UNIQUE: un pedido no puede tener dos certificados (R3, E-02, ADR-001). Es la
    # segunda barrera si fallara el bloqueo por fila del caso de uso.
    solicitud_id = models.BigIntegerField(unique=True)
    tipo_certificado = models.CharField(max_length=30)
    # Solo los datos mínimos para la verificación pública (R1); las calificaciones
    # no se guardan, solo van dentro del PDF (ADR-002).
    nombres_titular = models.CharField(max_length=150)
    fecha_emision = models.DateField(auto_now_add=True)
    codigo = models.CharField(max_length=80, unique=True, null=True)

    class Meta:
        db_table = "emision_certificado"
