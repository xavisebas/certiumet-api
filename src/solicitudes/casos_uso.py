"""Casos de uso CU-01 a CU-04. Solo conocen el dominio y los puertos (ADR-003)."""

from __future__ import annotations

from solicitudes.dominio import (
    ConflictoEstado,
    DatosInvalidos,
    Estado,
    NoEncontrado,
    SinPermiso,
    Solicitud,
    Usuario,
    validar_tipo_certificado,
)
from solicitudes.puertos import Bitacora, EmisorCertificados, RepositorioSolicitudes, UnidadDeTrabajo

APROBAR = "APROBAR"
RECHAZAR = "RECHAZAR"


def crear_solicitud(
    usuario: Usuario, tipo_certificado: object, repo: RepositorioSolicitudes, bitacora: Bitacora, ip: str | None
) -> Solicitud:
    """CU-01 · HU-01. El pedido empieza en EN_VALIDACION; la validación contra el
    sistema académico se hace después (E-06), así una caída no hace perder pedidos."""
    if usuario.es_funcionario:
        raise SinPermiso("Solo un estudiante puede pedir un certificado.")
    tipo = validar_tipo_certificado(tipo_certificado)
    solicitud = repo.crear(usuario.id, tipo)
    bitacora.registrar(usuario.id, "CREAR_SOLICITUD", f"solicitud:{solicitud.id}", ip)
    return solicitud


def _obtener_propia(
    usuario: Usuario, id_solicitud: int, repo: RepositorioSolicitudes, bitacora: Bitacora, ip: str | None
) -> Solicitud:
    """Control de acceso por dueño en un solo punto (E-01). Si el pedido es ajeno se
    responde igual que si no existiera, y el intento queda en la bitácora (E-04)."""
    solicitud = repo.obtener(id_solicitud)
    if solicitud is None or not (usuario.es_funcionario or solicitud.pertenece_a(usuario)):
        bitacora.registrar(usuario.id, "ACCESO_DENEGADO", f"solicitud:{id_solicitud}", ip)
        raise NoEncontrado()
    return solicitud


def consultar_solicitud(
    usuario: Usuario, id_solicitud: int, repo: RepositorioSolicitudes, bitacora: Bitacora, ip: str | None
) -> Solicitud:
    """CU-02 · HU-02."""
    solicitud = _obtener_propia(usuario, id_solicitud, repo, bitacora, ip)
    bitacora.registrar(usuario.id, "CONSULTAR_SOLICITUD", f"solicitud:{id_solicitud}", ip)
    return solicitud


def resolver_solicitud(
    usuario: Usuario,
    id_solicitud: int,
    decision: object,
    motivo: str | None,
    repo: RepositorioSolicitudes,
    bitacora: Bitacora,
    emisor: EmisorCertificados,
    uow: UnidadDeTrabajo,
    ip: str | None,
) -> Solicitud:
    """CU-03 · HU-03. La lectura con bloqueo, el cambio de estado, la emisión y la
    bitácora van en una sola transacción: la segunda aprobación simultánea espera, ve
    el pedido ya APROBADO y recibe 409 (E-02, ADR-001)."""
    if not usuario.es_funcionario:
        raise SinPermiso("Solo un funcionario de Secretaría puede resolver pedidos.")
    if decision not in (APROBAR, RECHAZAR):
        raise DatosInvalidos("La decisión debe ser APROBAR o RECHAZAR.")
    with uow.transaccion():
        solicitud = repo.obtener_para_actualizar(id_solicitud)
        if solicitud is None:
            raise NoEncontrado()
        if decision == APROBAR:
            solicitud.aprobar()
            solicitud.codigo_verificacion = emisor.emitir(solicitud)
        else:
            solicitud.rechazar(motivo)
        repo.guardar(solicitud)
        bitacora.registrar(usuario.id, f"RESOLVER_{decision}", f"solicitud:{id_solicitud}", ip)
    return solicitud


def descargar_certificado(
    usuario: Usuario,
    id_solicitud: int,
    repo: RepositorioSolicitudes,
    bitacora: Bitacora,
    emisor: EmisorCertificados,
    ip: str | None,
) -> bytes:
    """CU-04 · HU-04."""
    solicitud = _obtener_propia(usuario, id_solicitud, repo, bitacora, ip)
    if solicitud.estado != Estado.APROBADO:
        raise ConflictoEstado(solicitud.estado, "El certificado todavía no ha sido emitido.")
    pdf = emisor.generar_pdf(solicitud)
    bitacora.registrar(usuario.id, "DESCARGAR_CERTIFICADO", f"solicitud:{id_solicitud}", ip)
    return pdf
