"""Prueba de humo del esqueleto ejecutable (rúbrica semana 4, criterio 4).

Llama a la API ya levantada (python manage.py runserver) y recorre el caso principal:
  1. E-01: sin token, la API no muestra un pedido (401).
  2. HU-01 / CA-01.1: un estudiante pide un certificado de matrícula (201).
  3. HU-02: el mismo estudiante consulta su pedido (200).
  4. HU-05 / CA-05.2: un código alterado responde 200 con "valido" en falso.

Uso:  python scripts/prueba_humo.py [URL_BASE]   (por defecto http://127.0.0.1:8000)
El token se genera con la clave de desarrollo del proyecto (supuesto A2); no usa secretos reales.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from config.autenticacion import emitir_token  # noqa: E402

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")


def llamar(metodo, ruta, token=None, cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    peticion = urllib.request.Request(BASE + ruta, data=datos, method=metodo)
    peticion.add_header("Content-Type", "application/json")
    if token:
        peticion.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(peticion, timeout=10) as respuesta:
            return respuesta.status, json.loads(respuesta.read() or b"{}")
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read() or b"{}")


def comprobar(nombre, obtenido, esperado):
    estado = "OK " if obtenido == esperado else "FALLA"
    print(f"[{estado}] {nombre}: esperado {esperado}, obtenido {obtenido}")
    return obtenido == esperado


def main():
    token = emitir_token(9001, "ESTUDIANTE", "Estudiante de prueba")
    resultados = []

    codigo, _ = llamar("GET", "/api/v1/solicitudes/1")
    resultados.append(comprobar("E-01 sin token no se muestra el pedido", codigo, 401))

    codigo, cuerpo = llamar("POST", "/api/v1/solicitudes", token, {"tipoCertificado": "MATRICULA"})
    resultados.append(comprobar("HU-01 CA-01.1 pedir certificado de matrícula", codigo, 201))

    pedido = cuerpo.get("id")
    codigo, _ = llamar("GET", f"/api/v1/solicitudes/{pedido}", token)
    resultados.append(comprobar("HU-02 consultar el pedido propio", codigo, 200))

    codigo, cuerpo = llamar("GET", "/api/v1/verificaciones/CODIGO-ALTERADO")
    resultados.append(comprobar("HU-05 CA-05.2 código alterado (estado HTTP)", codigo, 200))
    resultados.append(comprobar("HU-05 CA-05.2 código alterado (valido)", cuerpo.get("valido"), False))

    if not all(resultados):
        sys.exit(1)
    print("Prueba de humo superada: el esqueleto corre de punta a punta.")


if __name__ == "__main__":
    main()
