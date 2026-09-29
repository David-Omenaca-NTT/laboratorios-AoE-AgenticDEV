"""Carga de catalogos de categorias y politicas de capacidad, versionados."""
from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from ..dominio.modelos import Categoria, CatalogoCategorias
from .motor import Politica

RAIZ = Path(__file__).resolve().parents[3]
RUTA_CATEGORIAS = RAIZ / "politicas" / "categorias"
RUTA_CAPACIDAD = RAIZ / "politicas" / "capacidad"


def _fecha(valor):
    return date.fromisoformat(valor) if valor else None


def cargar_catalogo(version: str, ruta: Path = None) -> CatalogoCategorias:
    base = ruta or RUTA_CATEGORIAS
    datos = json.loads((base / ("%s.json" % version)).read_text(encoding="utf-8"))
    categorias = {
        c["codigo"]: Categoria(
            codigo=c["codigo"], nombre=c["nombre"],
            orden_seniority=c["orden_seniority"],
            utilizacion_objetivo=Decimal(str(c["utilizacion_objetivo"])),
            capacidad_facturable_esperada=Decimal(str(c["capacidad_facturable_esperada"])),
            vigente_desde=_fecha(c["vigente_desde"]),
            vigente_hasta=_fecha(c.get("vigente_hasta")))
        for c in datos["categorias"]
    }
    return CatalogoCategorias(version=datos["version"],
                              vigente_desde=_fecha(datos["vigente_desde"]),
                              categorias=categorias)


def catalogo_vigente_en(momento: date, ruta: Path = None) -> CatalogoCategorias:
    """El catalogo que aplicaba en una fecha dada. Un catalogo de 2025 no se
    aplica a una asignacion de 2027, y al reves tampoco."""
    base = ruta or RUTA_CATEGORIAS
    candidatos = []
    for fichero in sorted(base.glob("*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        desde = _fecha(datos["vigente_desde"])
        if desde <= momento:
            candidatos.append((desde, datos["version"]))
    if not candidatos:
        raise ValueError("no hay catalogo vigente en %s" % momento)
    return cargar_catalogo(max(candidatos)[1], base)


def cargar_politica(version: str, ruta: Path = None) -> Politica:
    base = ruta or RUTA_CAPACIDAD
    datos = json.loads((base / ("%s.json" % version)).read_text(encoding="utf-8"))
    return Politica(version=datos["version"],
                    tolerancia_sobreasignacion_pct=datos["tolerancia_sobreasignacion_pct"],
                    permite_sobreasignacion=datos["permite_sobreasignacion"],
                    dedicaciones_validas=tuple(datos["dedicaciones_validas"]))
