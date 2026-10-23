from django.db import models

from solicitudes.dominio import TIPOS_CERTIFICADO, Estado


class SolicitudModelo(models.Model):
    ESTADOS = [(e, e) for e in (Estado.EN_VALIDACION, Estado.VALIDADO, Estado.APROBADO, Estado.RECHAZADO)]
    TIPOS = [(t, t) for t in TIPOS_CERTIFICADO]

    numero_tramite = models.CharField(max_length=30, unique=True, null=True)
    # Identificador interno del estudiante que viene en su token; no es la cédula (R1).
    estudiante_id = models.BigIntegerField(db_index=True)
    tipo_certificado = models.CharField(max_length=30, choices=TIPOS)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=Estado.EN_VALIDACION)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    motivo_rechazo = models.CharField(max_length=300, null=True, blank=True)
    codigo_verificacion = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        db_table = "solicitudes_solicitud"
