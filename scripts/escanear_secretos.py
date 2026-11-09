"""Escaneo de secretos en los archivos versionados (quality gate "seguridad").

Recorre los archivos que Git versiona (git ls-files) y busca patrones de credenciales:
claves de AWS, tokens de GitHub, claves privadas y asignaciones literales de contraseñas,
tokens o claves. Termina con código 1 si encuentra alguno.

Una línea se puede excluir de forma explícita con el comentario "escaneo-secretos: permitido",
solo para valores de desarrollo que no son credenciales reales (por ejemplo, la base temporal del CI).
"""

import re
import subprocess
import sys

PATRONES = {
    "Clave de acceso de AWS": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Token personal de GitHub": re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|github_pat_[A-Za-z0-9_]{22,}"),
    "Clave privada": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "Token de Slack": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "Asignación literal de secreto": re.compile(
        r"""(?i)\b(password|passwd|contrase(n|ñ)a|secret|token|api_?key|clave)\b\s*[:=]\s*["'][^"'\s$<{]{8,}["']"""
    ),
}
PERMITIDO = "escaneo-secretos: permitido"
EXTENSIONES_BINARIAS = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".zip", ".docx", ".xlsx")


def archivos_versionados():
    salida = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return [r for r in salida.splitlines() if r and not r.lower().endswith(EXTENSIONES_BINARIAS)]


def main():
    hallazgos = []
    archivos = archivos_versionados()
    for ruta in archivos:
        try:
            with open(ruta, encoding="utf-8") as archivo:
                lineas = archivo.readlines()
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        for numero, linea in enumerate(lineas, start=1):
            if PERMITIDO in linea:
                continue
            for nombre, patron in PATRONES.items():
                if patron.search(linea):
                    hallazgos.append(f"{ruta}:{numero}: {nombre}")
    if hallazgos:
        print("Posibles secretos encontrados:")
        print("\n".join(hallazgos))
        sys.exit(1)
    print(f"Sin secretos detectados en {len(archivos)} archivos versionados.")


if __name__ == "__main__":
    main()
