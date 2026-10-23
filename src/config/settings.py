"""Configuración de Django para CertiUMET (esqueleto ejecutable, semana 2).

Los valores sensibles se leen de variables de entorno. Los valores por defecto solo
sirven para desarrollo local y pruebas; no son credenciales reales (supuesto A4).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "solo-desarrollo-no-usar-en-produccion")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "rest_framework",
    "solicitudes",
    "emision",
    "auditoria",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
APPEND_SLASH = False

# Base de datos: PostgreSQL 16 (ADR-001) cuando existe POSTGRES_DB.
# Sin esa variable se usa SQLite solo para pruebas rápidas; la prueba de
# concurrencia de E-02 exige PostgreSQL y se omite con SQLite.
if os.environ.get("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["POSTGRES_DB"],
            "USER": os.environ.get("POSTGRES_USER", "certiumet"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "desarrollo.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["config.autenticacion.AutenticacionToken"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "EXCEPTION_HANDLER": "config.errores.manejar_excepcion",
    "UNAUTHENTICATED_USER": None,
}

# Token del sistema de usuarios de la universidad, simulado con JWT (supuesto A2).
JWT_CLAVE = os.environ.get("JWT_CLAVE", "clave-jwt-solo-para-desarrollo-local-y-pruebas")

# Clave para firmar los códigos de verificación de certificados (E-03).
CLAVE_FIRMA_CERTIFICADOS = os.environ.get("CLAVE_FIRMA_CERTIFICADOS", "clave-firma-solo-para-desarrollo-y-pruebas")

# Adaptador del sistema académico (ADR-002): "simulado" en el proyecto.
ADAPTADOR_ACADEMICO = os.environ.get("ADAPTADOR_ACADEMICO", "simulado")
