"""Servicio HTTP de Abaco.

FastAPI es la unica dependencia externa y vive solo en esta capa: el dominio y
las reglas se ejecutan y se testean sin levantar nada.

Arquitectura: monolito modular con fronteras limpias. El PRD pedia
microservicios, Kafka y CQRS. Para este alcance eso seria sobreingenieria, y
defender esta eleccion ante el panel es parte del ejercicio.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timezone

from ..dominio.estados import exigir_admite_asignacion, transicionar
from ..dominio.modelos import Demanda, EstadoDemanda, Posicion
from ..reglas.motor import evaluar_candidato
from ..reglas.ocupacion import utilizacion, utilizacion_agregada
from ..reglas.politicas import cargar_politica, catalogo_vigente_en

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("abaco.api")

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError:
    FastAPI = None

_DEMANDAS: dict = {}

if FastAPI is not None:
    app = FastAPI(title="Abaco", version="1.0.0")

    class PosicionEntrada(BaseModel):
        rol: str
        codigo_categoria: str
        skill: str
        nivel_minimo: int
        dedicacion_pct: int

    class DemandaEntrada(BaseModel):
        demanda_id: str
        proyecto: str
        solicitante: str
        posiciones: list
        desde: str
        hasta: str
        prioridad: str = "media"

    @app.get("/salud")
    def salud():
        return {"estado": "ok", "momento": datetime.now(timezone.utc).isoformat()}

    @app.post("/demandas")
    def crear_demanda(entrada: DemandaEntrada):
        log.info("alta de demanda %s con %d posiciones",
                 entrada.demanda_id, len(entrada.posiciones))
        if entrada.demanda_id in _DEMANDAS:
            raise HTTPException(status_code=409, detail="la demanda ya existe")
        demanda = Demanda(
            demanda_id=entrada.demanda_id, proyecto=entrada.proyecto,
            solicitante=entrada.solicitante,
            posiciones=[Posicion(**p) for p in entrada.posiciones],
            desde=date.fromisoformat(entrada.desde),
            hasta=date.fromisoformat(entrada.hasta),
            prioridad=entrada.prioridad,
            momento_solicitud=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        _DEMANDAS[demanda.demanda_id] = demanda
        return {"demanda_id": demanda.demanda_id, "estado": demanda.estado.value}

    @app.post("/demandas/{demanda_id}/transicion")
    def transicion(demanda_id: str, destino: str):
        demanda = _DEMANDAS.get(demanda_id)
        if demanda is None:
            raise HTTPException(status_code=404, detail="demanda no encontrada")
        try:
            transicionar(demanda, EstadoDemanda(destino))
        except Exception as exc:
            log.warning("transicion rechazada en %s: %s", demanda_id, exc)
            raise HTTPException(status_code=409, detail=str(exc))
        return {"demanda_id": demanda_id, "estado": demanda.estado.value}

    @app.get("/demandas/{demanda_id}")
    def ver_demanda(demanda_id: str):
        demanda = _DEMANDAS.get(demanda_id)
        if demanda is None:
            raise HTTPException(status_code=404, detail="demanda no encontrada")
        exigir_admite_asignacion(demanda) if demanda.estado not in (
            EstadoDemanda.CERRADA, EstadoDemanda.CANCELADA) else None
        return {"demanda_id": demanda_id, "estado": demanda.estado.value,
                "posiciones": len(demanda.posiciones)}
