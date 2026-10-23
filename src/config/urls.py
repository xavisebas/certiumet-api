"""Rutas de la API. Coinciden con los paths de api/openapi.yaml."""

from django.urls import path

from emision import vistas as vistas_emision
from solicitudes import vistas as vistas_solicitudes

urlpatterns = [
    path("api/v1/solicitudes", vistas_solicitudes.SolicitudesVista.as_view()),
    path("api/v1/solicitudes/<int:id>", vistas_solicitudes.SolicitudDetalleVista.as_view()),
    path(
        "api/v1/solicitudes/<int:id>/resolucion",
        vistas_solicitudes.ResolucionVista.as_view(),
    ),
    path(
        "api/v1/solicitudes/<int:id>/certificado",
        vistas_emision.CertificadoVista.as_view(),
    ),
    path("api/v1/verificaciones/<str:codigo>", vistas_emision.VerificacionVista.as_view()),
]
