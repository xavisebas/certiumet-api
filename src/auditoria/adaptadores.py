"""Adaptador de la bitácora de auditoría (puerto Bitacora)."""

from __future__ import annotations

from auditoria.models import RegistroAuditoria


class BitacoraDjango:
    def registrar(self, usuario_id: int | None, accion: str, recurso: str, ip: str | None) -> None:
        RegistroAuditoria.objects.create(usuario_id=usuario_id, accion=accion, recurso=recurso, ip=ip)
