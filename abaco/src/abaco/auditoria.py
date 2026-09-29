"""Traza de auditoria.

Invariante del contrato de contexto: toda decision de asignacion registra la
version de politica y de catalogo de categorias aplicadas, y ademas el ORIGEN
de la decision.

Ese campo `origen` no es decorativo. El defecto mas peligroso de este dominio
es que el sistema audite lo que hacen las personas y deje de auditar lo que
hace el agente. Aqui las dos rutas escriben la misma traza o no escribe ninguna.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

RUTA_TRAZA = Path(os.environ.get("ABACO_TRAZA", ".abaco/auditoria.jsonl"))

ORIGENES = ("api", "agente", "carga", "correccion_manual")


class OrigenInvalido(Exception):
    pass


def registrar_decision(entidad: str, entidad_id: str, accion: str, actor: str,
                       origen: str, version_politica: str, version_catalogo: str,
                       momento: str, detalle: dict) -> dict:
    if origen not in ORIGENES:
        raise OrigenInvalido("origen '%s' no valido, debe ser uno de %s"
                             % (origen, ", ".join(ORIGENES)))
    entrada = {
        "entidad": entidad,
        "entidad_id": entidad_id,
        "accion": accion,
        "actor": actor,
        "origen": origen,
        "version_politica": version_politica,
        "version_catalogo": version_catalogo,
        "momento": momento,
        "detalle": detalle,
    }
    RUTA_TRAZA.parent.mkdir(parents=True, exist_ok=True)
    with RUTA_TRAZA.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entrada, ensure_ascii=False, default=str) + "\n")
    return entrada


def leer_traza(ruta: Path = None) -> list:
    ruta = ruta or RUTA_TRAZA
    if not ruta.exists():
        return []
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]
