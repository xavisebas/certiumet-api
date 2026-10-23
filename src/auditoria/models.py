from django.db import models


class RegistroNoModificable(Exception):
    """La bitácora no se puede editar ni borrar (E-04)."""


class RegistroAuditoria(models.Model):
    # Los cinco campos que pide E-04: usuario, acción, recurso, fecha y hora, dirección IP.
    usuario_id = models.BigIntegerField(null=True)
    accion = models.CharField(max_length=40)
    recurso = models.CharField(max_length=80)
    fecha_hora = models.DateTimeField(auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField(null=True)

    class Meta:
        db_table = "auditoria_registro"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise RegistroNoModificable("Los registros de la bitácora no se pueden modificar.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise RegistroNoModificable("Los registros de la bitácora no se pueden borrar.")
