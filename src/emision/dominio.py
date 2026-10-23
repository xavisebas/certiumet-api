"""Firma y verificación del código de un certificado (E-03). Sin Django (ADR-003).

El código tiene la forma "<id del certificado>-<firma>", donde la firma es un HMAC-SHA256
recortado a 20 caracteres. Si se cambia un solo carácter, la firma deja de coincidir.
"""

from __future__ import annotations

import hashlib
import hmac

LARGO_FIRMA = 20


def _firma(id_certificado: int, clave: str) -> str:
    mensaje = f"certiumet:{id_certificado}".encode()
    return hmac.new(clave.encode(), mensaje, hashlib.sha256).hexdigest()[:LARGO_FIRMA]


def firmar(id_certificado: int, clave: str) -> str:
    return f"{id_certificado}-{_firma(id_certificado, clave)}"


def leer_codigo(codigo: str, clave: str) -> int | None:
    """Devuelve el id del certificado si la firma es auténtica; si no, None."""
    partes = codigo.split("-")
    if len(partes) != 2 or not partes[0].isdigit():
        return None
    id_certificado = int(partes[0])
    if not hmac.compare_digest(partes[1], _firma(id_certificado, clave)):
        return None
    return id_certificado
