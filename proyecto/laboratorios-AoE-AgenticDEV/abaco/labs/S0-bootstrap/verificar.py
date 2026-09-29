"""Verificador de S0: Bootstrap y disciplina de repositorio."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)


import re

# Patrones de dato personal que no pueden aparecer en el repositorio de
# aprendizaje. La prohibicion no se confia a una instruccion del contrato de
# contexto: se comprueba.
PATRONES_PERSONALES = [
    (r"\b[\w.+-]+@(?!ejemplo\.|example\.)[\w-]+\.[\w.]+\b", "correo electronico real"),
    (r"\b\d{8}[A-HJ-NP-TV-Z]\b", "DNI"),
    (r"\b(?:\+34|0034)?[\s-]?[6-7]\d{8}\b", "telefono movil"),
]

RUTAS_A_ESCANEAR = ["tests", "datos", "evals", "labs", "specs"]


def escanear_datos_personales():
    hallazgos = []
    for carpeta in RUTAS_A_ESCANEAR:
        base = RAIZ / carpeta
        if not base.exists():
            continue
        for fichero in base.rglob("*"):
            if not fichero.is_file() or fichero.suffix not in (".py", ".json", ".md", ".csv"):
                continue
            try:
                texto = fichero.read_text(encoding="utf-8")
            except Exception:
                continue
            for patron, etiqueta in PATRONES_PERSONALES:
                m = re.search(patron, texto)
                if m:
                    hallazgos.append("%s en %s: %s"
                                     % (etiqueta, fichero.relative_to(RAIZ), m.group(0)[:20]))
    return hallazgos


def verificar():
    c = []
    c.append(criterio("S0-01", "existe la plantilla de PR con la checklist",
                      existe(".github/pull_request_template.md")
                      and contiene(".github/pull_request_template.md", r"defenderlo ante"),
                      "falta la plantilla o la checklist"))
    c.append(criterio("S0-02", "CODEOWNERS protege labs, manifiestos y workflows",
                      existe(".github/CODEOWNERS")
                      and contiene(".github/CODEOWNERS", r"labs/")
                      and contiene(".github/CODEOWNERS", r"manifiestos/"),
                      "CODEOWNERS no cubre las rutas prohibidas del contrato de contexto"))
    c.append(criterio("S0-03", "el pipeline incluye el gate de tamano de PR",
                      contiene(".github/workflows/ci.yml", r"tamano-pr|LIMITE_LINEAS"),
                      "no hay job que limite el tamano del diff"))
    c.append(criterio("S0-04", "el pipeline ejecuta la suite",
                      contiene(".github/workflows/ci.yml", r"pytest"),
                      "el workflow no ejecuta los tests"))

    hallazgos = escanear_datos_personales()
    c.append(criterio("S0-05",
                      "NINGUN dato personal real en el repositorio de aprendizaje",
                      not hallazgos,
                      "; ".join(hallazgos[:3]) if hallazgos else ""))

    c.append(criterio("S0-06", "el contrato de contexto prohibe copiar datos reales",
                      contiene("CLAUDE.md", r"dato[s]? personal"),
                      "CLAUDE.md no declara la prohibicion de datos personales"))

    p = ejecutar(["git", "log", "--oneline"])
    commits = len(p.stdout.strip().splitlines()) if p.returncode == 0 else 0
    c.append(criterio("S0-07", "hay historial de git con al menos dos commits",
                      commits >= 2, "commits encontrados: %d" % commits))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
