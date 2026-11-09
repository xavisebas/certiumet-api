"""Métricas aproximadas tipo DORA a partir del historial de Git (rúbrica semana 4).

Fuente de datos: solo el historial de la rama main (no necesita la API de GitHub).
- Cada merge de un pull request en main cuenta como una "integración" (en el proyecto no hay
  despliegue a producción; la integración en main es el equivalente más cercano).
- Cada etiqueta vX.Y.Z cuenta como una "entrega" (release).

Métricas (Forsgren et al., 2018, adaptadas):
1. Frecuencia: integraciones por semana desde el primer pull request y entregas por semana.
2. Tiempo de entrega de cambios: desde el primer commit de la rama hasta su merge en main.
3. Tasa de fallos de cambios: pull requests cuya rama tuvo una falla en el pipeline que obligó a
   corregir antes del merge. Se detecta por el mensaje del commit ("falla provocada", "revert",
   "corrige ... ci/lint/pipeline"). Se contrasta a mano con la pestaña Actions de GitHub.
4. Tiempo de recuperación: desde el commit que rompió el pipeline hasta el commit que lo corrigió.
5. Tasa de retrabajo: pull requests de tipo fix sobre el total de pull requests.

Uso:  python scripts/metricas_dora.py > docs/evidencias/semana4/metricas-dora.md
"""

import re
import statistics
import subprocess
from datetime import datetime

PATRON_MERGE = re.compile(r"Merge pull request #(\d+)")
PATRON_FALLA = re.compile(r"(?i)falla provocada|revert|corrige .*(ci|pipeline|lint|falla)")
PATRON_TAG = re.compile(r"^v\d+\.\d+\.\d+$")


def git(*argumentos):
    return subprocess.run(["git", *argumentos], capture_output=True, text=True, check=True).stdout.strip()


def fecha(texto):
    return datetime.fromisoformat(texto)


def horas(delta):
    return delta.total_seconds() / 3600


def commits_de_rama(merge):
    """Commits que trajo el pull request: los de la rama que no estaban en main."""
    salida = git("log", "--reverse", "--format=%h|%aI|%s", f"{merge}^1..{merge}^2")
    return [linea.split("|", 2) for linea in salida.splitlines() if linea]


def main():
    merges = []
    for linea in git("log", "--first-parent", "main", "--merges", "--format=%h|%cI|%s").splitlines():
        sha, cuando, asunto = linea.split("|", 2)
        coincide = PATRON_MERGE.search(asunto)
        if coincide:
            merges.append({"sha": sha, "fecha": fecha(cuando), "pr": int(coincide.group(1))})
    merges.sort(key=lambda m: m["fecha"])

    filas, tiempos_entrega, recuperaciones = [], [], []
    prs_con_falla, prs_fix = 0, 0
    for merge in merges:
        commits = commits_de_rama(merge["sha"])
        if not commits:
            continue
        primero = fecha(commits[0][1])
        entrega = horas(merge["fecha"] - primero)
        tiempos_entrega.append(entrega)
        tipo = commits[0][2].split(":")[0].split("(")[0]
        if tipo == "fix" or any(c[2].startswith("fix") for c in commits):
            prs_fix += 1
        falla = "no"
        for indice, (_, cuando, asunto) in enumerate(commits):
            if PATRON_FALLA.search(asunto) and indice + 1 < len(commits):
                recuperaciones.append(horas(fecha(commits[indice + 1][1]) - fecha(cuando)))
                falla = "sí"
        if falla == "sí":
            prs_con_falla += 1
        filas.append(
            f"| #{merge['pr']} | {merge['sha']} | {merge['fecha']:%d/%m/%Y %H:%M} | {len(commits)} | {entrega:.1f} | {falla} |"
        )

    etiquetas = sorted(
        (
            (t, fecha(git("log", "-1", "--format=%cI", t)))
            for t in git("tag").splitlines()
            if PATRON_TAG.match(t)
        ),
        key=lambda par: par[1],
    )
    primer_commit = fecha(git("log", "--reverse", "--format=%cI", "main").splitlines()[0])
    ultimo = merges[-1]["fecha"] if merges else primer_commit
    semanas_flujo = max(horas(ultimo - merges[0]["fecha"]) / 168, 1 / 7) if merges else 1
    semanas_total = max(horas(ultimo - primer_commit) / 168, 1 / 7)

    total = len(tiempos_entrega)
    print("# Métricas aproximadas tipo DORA · CertiUMET API\n")
    print(f"Generado el {datetime.now():%d/%m/%Y %H:%M} con `python scripts/metricas_dora.py` sobre la rama main.\n")
    print("## Pull requests integrados en main\n")
    print("| PR | Merge | Fecha del merge | Commits | Tiempo de entrega (h) | Falla en el pipeline |")
    print("|---|---|---|---|---|---|")
    print("\n".join(filas))
    print("\n## Entregas (etiquetas SemVer)\n")
    print("| Etiqueta | Fecha |")
    print("|---|---|")
    for nombre, cuando in etiquetas:
        print(f"| `{nombre}` | {cuando:%d/%m/%Y %H:%M} |")
    print("\n## Resumen\n")
    print("| Métrica | Valor | Cómo se calculó |")
    print("|---|---|---|")
    print(
        f"| Frecuencia de integración | {total / semanas_flujo:.1f} PR por semana "
        f"({total} PR en {semanas_flujo:.1f} semanas) | Merges de PR en main desde el primer PR |"
    )
    print(
        f"| Frecuencia de entrega | {len(etiquetas) / semanas_total:.1f} versiones por semana "
        f"({len(etiquetas)} en {semanas_total:.1f} semanas) | Etiquetas vX.Y.Z desde el primer commit |"
    )
    if tiempos_entrega:
        print(
            f"| Tiempo de entrega de cambios | mediana {statistics.median(tiempos_entrega):.1f} h "
            f"(mín. {min(tiempos_entrega):.1f} h, máx. {max(tiempos_entrega):.1f} h) | "
            "Primer commit de la rama → merge en main |"
        )
    tasa = 100 * prs_con_falla / total if total else 0
    print(
        f"| Tasa de fallos de cambios | {tasa:.0f} % ({prs_con_falla} de {total} PR) | "
        "PR con una falla del pipeline corregida antes del merge |"
    )
    if recuperaciones:
        print(
            f"| Tiempo de recuperación | {statistics.median(recuperaciones) * 60:.0f} min | "
            "Commit que rompió el pipeline → commit que lo corrigió |"
        )
    else:
        print("| Tiempo de recuperación | sin datos | No hubo fallas registradas en el historial |")
    retrabajo = 100 * prs_fix / total if total else 0
    print(f"| Tasa de retrabajo | {retrabajo:.0f} % ({prs_fix} de {total} PR) | PR con commits de tipo fix |")


if __name__ == "__main__":
    main()
