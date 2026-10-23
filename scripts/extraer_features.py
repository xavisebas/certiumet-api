"""Copia los bloques Gherkin de docs/07-historias-y-criterios.md a tests/features/.

Así los criterios se escriben una sola vez (en el 07) y las pruebas usan exactamente
el mismo texto (tareas T01 y T02 del mapa de toolchain). Uso, desde la raíz:

    python scripts/extraer_features.py          # genera los archivos
    python scripts/extraer_features.py --check  # falla si los .feature están desactualizados
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEN = RAIZ / "docs" / "07-historias-y-criterios.md"
DESTINO = RAIZ / "tests" / "features"


def bloques() -> dict[str, str]:
    texto = ORIGEN.read_text(encoding="utf-8")
    resultado = {}
    for bloque in re.findall(r"```gherkin\n(.*?)```", texto, re.S):
        historia = re.search(r"@HU-(\d+)", bloque)
        if not historia:
            raise SystemExit("Un bloque Gherkin del 07 no tiene la etiqueta @HU-nn.")
        resultado[f"hu{historia.group(1)}.feature"] = bloque
    return resultado


def main() -> int:
    revisar = "--check" in sys.argv
    DESTINO.mkdir(parents=True, exist_ok=True)
    diferencias = []
    for nombre, contenido in bloques().items():
        archivo = DESTINO / nombre
        if revisar:
            if not archivo.exists() or archivo.read_text(encoding="utf-8") != contenido:
                diferencias.append(nombre)
        else:
            archivo.write_text(contenido, encoding="utf-8")
            print(f"Generado: {archivo.relative_to(RAIZ)}")
    if diferencias:
        print("Desactualizados respecto al 07: " + ", ".join(diferencias))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
