from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EXTENSIONES = {".py", ".json", ".yaml", ".yml", ".md", ".csv", ".toml", ".txt"}
PATRONES = [
    (re.compile(r"\b[\w.+-]+@(?!ejemplo\.|example\.)[\w-]+\.[\w.]+\b", re.I), "correo electronico real"),
    (re.compile(r"\b\d{8}[A-HJ-NP-TV-Z]\b", re.I), "DNI"),
    (re.compile(r"\b(?:\+34|0034)?[\s-]?[6-7]\d{8}\b"), "telefono movil"),
]
EXCLUIDOS = {".git", ".venv", "__pycache__", "referencia"}


def hallazgos() -> list[str]:
    encontrados = []
    for fichero in RAIZ.rglob("*"):
        if not fichero.is_file() or fichero.suffix.lower() not in EXTENSIONES:
            continue
        if any(parte in EXCLUIDOS for parte in fichero.relative_to(RAIZ).parts):
            continue
        try:
            texto = fichero.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for patron, etiqueta in PATRONES:
            coincidencia = patron.search(texto)
            if coincidencia:
                encontrados.append(
                    f"{etiqueta} en {fichero.relative_to(RAIZ)}: {coincidencia.group(0)[:40]}"
                )
    return encontrados


def main() -> int:
    encontrados = hallazgos()
    if encontrados:
        print("ERROR: posibles datos personales reales detectados")
        print("\n".join(encontrados))
        return 1
    print("OK: no se detectaron datos personales reales en archivos de texto")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
